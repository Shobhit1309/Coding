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

class SourceFileNotFoundError(Exception):
	""" class for source file not found error """
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
	
	logger.info('input params '+'-'*80)
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
			print(f'Error occured. File {filename2} not found. Exiting the program....')
		else:
			logger.exception(f'Error occured while reading and loading file {filename1} in dataframe')
			print(f'Error occured. File {filename1} not found. Exiting the program ....')
			sys.exit(1)
	except Exception as e:
		logger.exception('Error occured while reading and loading file in dataframes')
		print('An error occured while executing the program. Below are the details:')
		raise

def clean_data(df1,df2):
	""" This function is used to clean the data in dataframes 1 and 2 """
	try:
		''' finding duplicate id and replacing it with unique alphanumeric code
		  to maintain consistence and to join with other data frame '''
		logger.info('finding duplicate id and replacing it with unique alphanumeric code to maintain consistence and to join with other data frame')
		df1.loc[df1.duplicated(['id']),'id']='4903x34'

		''' merging df1 and df2 dataframes and creating a new one '''
		logger.info('merging df1 and df2 dataframes and creating a new one')
		new_df=pd.merge(df1, df2, on='id', how='outer')
		
		''' assigning 1 (female) to Sandrine after merging dataframes '''
		logger.info('assigning 1 (female) to Sandrine after merging dataframes')
		new_df.loc[new_df.first_name=='Sandrine',['sex']]='1'
		
		''' renaming columns as per API documentation '''
		logger.info('renaming columns as per API documentation')
		new_df.rename(index=str,\
			columns={"attr2":"phone_numbers","id":"external_id","sex":"gender","tier":"custom_1",\
			"lastcontact":"custom_2"},inplace=True)

		''' tranlating 0 and 1 to Male and Female '''
		logger.info('tranlating 0 and 1 to Male and Female')
		new_df['gender'] = np.where(new_df['gender'] ==0, 'm', 'f')

		''' dropping the below columns which are not required:
			# attr1_x from customer1.csv -- not making any sense 
			# engagement from customer1.csv -- not making any sense
			# pets from customer2.csv -- not making any sense
			# vehcle from customer2.csv -- not making any sense 
		'''
		logger.info('dropping the below columns which are not required:\n\
			attr1_x from customer1.csv, engagement from customer1.csv, pets from customer2.csv, vehcle from customer2.csv')
		new_df.drop(['attr1_x','engagement','pets','attr1_y'],inplace=True,axis =1)

		''' removing spaces from email id column '''
		logger.info('removing spaces from email id column')
		new_df['email']=new_df['email'].str.replace(' ','')

		''' adding the below columns as per session m API documentation
			# opted_in : defaults to true if no attribute value is specified hence true for all records
			# external_id_type : This represents from which platform the data is received "facebook,instagram etc".NaN for no details
			# locale : by looking at phone numbers since it's of USA so locale should be en-u for all records
			# ip : NaN for no details
			# dob : NaN for no details
			# address : NaN for no details
			# city : NaN for no details
			# state : NaN for no details
			# zip : NaN for no details
			# country : by looking at phone numbers since it's of USA so country should be USA for all records
			# referral : NaN for no details -- this can be generated while processing data using NAME-XXXXXX but kept blank as not received from source
			# phone_type : NaN for no details
		'''
		logger.info('additing the below columns as per sessionM API documentation\n\
			opted_in,external_id_type,locale,ip,dob,address,city,state,zip,country,referral,phone_type')
		
		new_df['opted_in'],new_df['external_id_type'],new_df['locale'],\
		new_df['ip'],new_df['dob'],new_df['address'],new_df['city'],\
		new_df['state'],new_df['zip'],new_df['country'],new_df['referral'],\
		new_df['phone_type']=[True,np.nan,'en-u',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'USA',np.nan,np.nan]

		''' correcting the date format present in custom_2 column '''
		logger.info('correcting the date format present in custom_2 column')
		new_df['custom_2'] = pd.to_datetime(new_df['custom_2']).dt.strftime('%Y-%m-%d')


		''' removing NaT from custom_2 field '''
		logger.info('removing NaT from custom_2 field')
		new_df['custom_2'] =  new_df['custom_2'].astype(str)
		new_df['custom_2'] = new_df['custom_2'].apply(lambda val : np.nan if val=="NaT" else val)

		''' arranging the columns in the order mentioned in API documentation '''
		logger.info('arranging the columns in the order mentioned in API documentation')
		new_df=new_df[['external_id','opted_in','external_id_type',\
		'email','locale','ip','dob','address','city','state','zip','country',\
		'gender','first_name','last_name','referral','phone_numbers','phone_type','custom_1','custom_2']]

		return new_df

	except Exception as e:
		logger.error('Error occured in the program:',e)
		raise


def export_csv(new_df):
	''' Exporting data in CSV '''
	logger.info('Exporting data in CSV: Combined_Customer_data.csv')
	new_df.to_csv('Combined_Customer_data.csv')


def main(argv=None):
	''' creating arg parse for reading inputs from command line '''
	if argv is None:
		argv=sys.argv
	args= parse_args(argv[1:])
	filename1 = args.source_file1
	filename2 = args.source_file2
	try:
		logger.info('Calling load_csv function to read csv and create dataframes')
		df1,df2=load_csv(filename1,filename2)

		logger.info('Calling clean_data function to clean data and create a new dataframe new_df')
		new_df=clean_data(df1,df2)

		logger.info('Calling export_data function to export the data in combined customer data csv file')
		export_csv(new_df)

		print('Process completed Successfully!! Combined Customer data file generated.')
		logger.info('Process completed Successfully!! Combined Customer data file generated.')
	except Exception as e:
		logger.error(f'Program failed !!')

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