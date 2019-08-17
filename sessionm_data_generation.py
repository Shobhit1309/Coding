#!/usr/bin/env python
#==========================================================================================
# title			 : sessionm_data_generation.py
# description    : The program reads customer data files,
#				   cleans the data and generate cleaned csv compatible to sessionm platform
# author 		 : Shobhit Bhatnagar
# date           : 2019-08-05
# version        : 1.0
# python version : 3.7.3
#==========================================================================================
import sys
import os
import pandas as pd
import numpy as np
import argparse
import logging
from datetime import datetime
from cryptography.fernet import Fernet

""" Setting the display properties of dataframe """
pd.set_option('display.max_columns',50)
pd.set_option('display.max_colwidth',500)


class SourceFileNotFoundError(Exception):
	""" class for source file not found error """
	pass

class InvalidRecordFound(Exception):
	""" class for Invalid record found error """
	pass



def create_parser():
	""" This function will return command line parser """
	parser=argparse.ArgumentParser(description='Script to clean the data and make it compatible to Sessionm platform',prog='sessionm_data_generation.py')
	parser.add_argument('--sourcefile1', dest='source_file1', help='source file name 1')
	parser.add_argument('--sourcefile2', dest='source_file2', help='source file name 2')
	parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
	return parser


def parse_args(arguments):
	""" This function will parse the command line arguments """
	parser=create_parser()
	args=parser.parse_args(arguments)

	''' check for mandatory parameters '''
	if not args.source_file1 or not args.source_file2:
		logger.error('Incorrect number of arguments: Source filename1 and filename2 are required')
		parser.error('Incorrect number of arguments: Source filename1 and filename2 are required')

	logger.info('Input params')
	logger.info('-'*80)
	logger.info(args)
	logger.info('-'*80)
	return args


def load_csv(filename1,filename2):
	""" This function is used to check the presence of files and load them into dataframes """
	try:
		File1_status=os.path.isfile(filename1)
		File2_status=os.path.isfile(filename2)

		if not File1_status or not File2_status:
			raise SourceFileNotFoundError
		else:
			df1=pd.read_csv(filename1)
			logger.info(filename1+' is loaded in df1 dataframe')
			df2=pd.read_csv(filename2)
			logger.info(filename2+' is loaded in df2 dataframe')
		return df1,df2

	except SourceFileNotFoundError as e:
		if File1_status:
			logger.exception(f'Error occured while reading and loading file {filename2} in dataframe')
			print(f' Error occured. File {filename2} not found. Exiting the program ....')
		else:
			logger.exception(f'Error occured while reading and loading file {filename1} in dataframe')
			print(f' Error occured. File {filename1} not found. Exiting the program ....')
			sys.exit(1)
	except Exception as e:
		logger.exception('Error occured while reading and loading file in dataframes')
		print(' An error occured while executing the program. Exiting the program ....')
		raise

def encrypt_txt(txt):
	""" This function is used to encrypt the text """
	try:
		key = Fernet.generate_key()
		f = Fernet(key)
		txt=bytes(txt,encoding='utf-8')
		token = f.encrypt(txt)
		enc_text=token.decode('utf-8')+'**ENC**'
		return enc_text
		logger.info('Text encryption done')
	except Exception as e:
		logger.error('Error occured:',e)
		raise

def clean_data(df1,df2):
	""" This function is used to clean the data in dataframes 1 and 2 """
	try:
		''' finding duplicate id and replacing it with unique alphanumeric code
		  to maintain consistence and to join with other data frame '''
		logger.info('Finding duplicate id and replacing it with unique alphanumeric code to maintain consistence and to join with other data frame')
		df1.loc[df1.duplicated(['id']),'id']='4903x34'

		''' merging df1 and df2 dataframes and creating a new one '''
		logger.info('Merging df1 and df2 dataframes and creating a new one')
		new_df=pd.merge(df1, df2, on='id', how='outer')
		
		''' assigning 1 (female) to Sandrine after merging dataframes '''
		logger.info('Assigning 1 (female) to Sandrine after merging dataframes')
		new_df.loc[new_df.first_name=='Sandrine','sex']=1
		
		''' renaming columns as per API documentation '''
		logger.info('Renaming columns as per API documentation')
		new_df.rename(index=str,\
			columns={"attr2":"phone_numbers","id":"external_id","sex":"gender","tier":"custom_1",\
			"lastcontact":"custom_2"},inplace=True)

		''' tranlating 0 to Male 1 to Female and other codes to invalid gender '''
		logger.info('Tranlating 0 to Male 1 to Female and other codes to invalid gender')
		
		condition =[(new_df['gender']==0),(new_df['gender'] ==1)]
		choices=['m','f']

		new_df['gender'] = np.select(condition,choices,default='invalid')

		''' dropping the below columns which are not required:
			# attr1_x from customer1.csv -- not making any sense 
			# engagement from customer1.csv -- not making any sense
			# pets from customer2.csv -- not making any sense
			# vehcle from customer2.csv -- not making any sense 
		'''
		logger.info('Dropping the below columns which are not required:\n\
			attr1_x from customer1.csv, engagement from customer1.csv, pets from customer2.csv, vehcle from customer2.csv')
		new_df.drop(['attr1_x','engagement','pets','attr1_y'],inplace=True,axis =1)

		''' removing spaces from email id column and encrypting the email ids '''
		logger.info('Removing spaces from email id column')
		new_df['email']=new_df['email'].str.replace(' ','')

		logger.info('Encrypting email ids')
		new_df['email']=new_df['email'].astype(str).apply(encrypt_txt)

		''' adding the below columns as per session m API documentation
			# opted_in : defaults to true if no attribute value is specified hence true for all records
			# external_id_type : This represents from which platform the data is received "facebook,instagram etc".NaN for no details
			# locale : NaN for no details. However it can de derived by looking at phone numbers since it's of USA so locale should be en-u for all records
			# ip : NaN for no details
			# dob : NaN for no details
			# address : NaN for no details
			# city : NaN for no details
			# state : NaN for no details
			# zip : NaN for no details
			# country : NaN for no details.However by looking at phone numbers since it's of USA so country should be USA for all records.
			# referral : NaN for no details -- this can be generated while processing data using NAME-XXXXXX but kept blank as not received from source
			# phone_type : NaN for no details
		'''
		logger.info('Additing the below columns as per sessionM API documentation\n\
			opted_in,external_id_type,locale,ip,dob,address,city,state,zip,country,referral,phone_type')
		
		new_df['opted_in'],new_df['external_id_type'],new_df['locale'],\
		new_df['ip'],new_df['dob'],new_df['address'],new_df['city'],\
		new_df['state'],new_df['zip'],new_df['country'],new_df['referral'],\
		new_df['phone_type']=[True,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]

		''' correcting the date format present in custom_2 column '''
		logger.info('Correcting the date format present in custom_2 column')
		new_df['custom_2'] = pd.to_datetime(new_df['custom_2']).dt.strftime('%Y-%m-%d')

		''' removing NaT from custom_2 field '''
		logger.info('Removing NaT from custom_2 field')
		new_df['custom_2'] =  new_df['custom_2'].astype(str)
		new_df['custom_2'] = new_df['custom_2'].apply(lambda val : np.nan if val=="NaT" else val)

		''' arranging the columns in the order mentioned in API documentation '''
		logger.info('Arranging the columns in the order mentioned in API documentation')
		new_df=new_df[['external_id','opted_in','external_id_type',\
		'email','locale','ip','dob','address','city','state','zip','country',\
		'gender','first_name','last_name','referral','phone_numbers','phone_type','custom_1','custom_2']]

		return new_df

	except Exception as e:
		logger.error('Error occured in the program:',e)
		raise

def data_validator(df):
	""" This function is used to validate the cleaned data before writing it to csv. This will check the below: 
	1) email must be encrypted
	2) gender must be M or F
	3) opted in must be true or false
	"""
	try:
		df['Valid_email'],df['Valid_gender'],df['Valid_Opted_in']=[np.nan,np.nan,np.nan]
		
		df['Valid_email'] = df['email'].str[-7:].apply(lambda x: 'Y' if x == '**ENC**' else 'N')
		
		df['Valid_gender'] = df['gender'].apply(lambda x: 'Y' if (x == 'm') or (x == 'f') else 'N')
		
		df['Valid_Opted_in'] = df['opted_in'].apply(lambda x: 'Y' if  (x is True) or (x is False)  else 'N')

		inv_df=df.loc[(df.Valid_email == 'N') | (df.Valid_gender == 'N') | (df.Valid_Opted_in == 'N'),:]

		if not inv_df.empty:
			raise InvalidRecordFound

	except InvalidRecordFound:
		logger.error('Data Sanity checks failed. Below are the invalid records\n')
		logger.error(inv_df)
		print(' Running data sanity checks on cleaned data: FAILED','\n Exiting the program ....')
		sys.exit(1)
	except Exception as e:
		logger.error(e)
		print('\n Error occured while running Data Sanity checks. Exiting the program ....')
		sys.exit(1)


def export_csv(new_df):
	try:
		''' Exporting data in CSV '''
		logger.info('Exporting data in CSV: Combined_Customer_data.csv')
		new_df.to_csv('Combined_Customer_data.csv',index=False)
		logger.info('Data exported in CSV!')
	except Exception as e:
		print(' ',e,': File already open. Please Close Combined_Customer_data.csv file and try again.')
		logger.error('File already open. Please Close Combined_Customer_data.csv file')
		sys.exit(1)

def main(argv=None):
	''' creating arg parse for reading inputs from command line '''
	if argv is None:
		argv=sys.argv
	args= parse_args(argv[1:])
	filename1 = args.source_file1
	filename2 = args.source_file2
	try:
		print('\n','-'*33,'SessionM-Data-Generation-Program','-'*33,'\n')
		print(' Program started on:',datetime.now().strftime("%b %d %Y %H:%M:%S"))
		logger.info('Calling load_csv function to read csv and create dataframes')
		df1,df2=load_csv(filename1,filename2)
		print(' Loading datafiles into dataframe: DONE')

		logger.info('Calling clean_data function to clean data and create a new dataframe new_df')
		new_df=clean_data(df1,df2)
		print(' Cleaning data: DONE')

		logger.info('Calling data_validator function to perform data sanity checks before exporting to csv file')
		data_validator(new_df)
		print(' Running data sanity checks on cleaned data: DONE')

		# Dropping Validation check columns from new_df before writing data to csv
		new_df.drop(['Valid_email', 'Valid_gender','Valid_Opted_in'], axis = 1,inplace=True) 

		logger.info('Calling export_data function to export the data in combined customer data csv file')
		export_csv(new_df)
		print(' Exporting data into Combined_Customer_data.csv: DONE')

		logger.info('Process completed Successfully!! Combined Customer data file generated.')
		print(' Process completed Successfully!')
		print(' Program ended on :',datetime.now().strftime("%b %d %Y %H:%M:%S"),'\n')
		print('','-'*100)
	except Exception as e:
		logger.error('Program failed !!\n',e)

''' Creating logger for program '''
log_file_name='sessionm_data_generation'
log_file_name +='_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.log'
logger=logging.getLogger(__name__) # getting the getLogger method from logging module and logger object is created for it.
logger.setLevel(logging.DEBUG) # setting the logging level of logger
formatter=logging.Formatter('%(asctime)s:%(levelname)s:%(message)s') # creating an object which will set the format of log file
file_handler=logging.FileHandler(log_file_name) # log file name
file_handler.setFormatter(formatter) # setting the format of log file using formatter object created above
logger.addHandler(file_handler) # adding handler for log file		


if __name__=="__main__":
	sys.exit(main())
