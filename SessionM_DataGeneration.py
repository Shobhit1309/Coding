import sys
import os
import pandas as pd
import numpy as np
import argparse

def load_csv(filename1,filename2):
	""" This function is used to check the presence of files and load them into dataframes """
	try:
		if not os.path.isfile(filename1) or not os.path.isfile(filename2):
    		raise FileNotFoundError
    	else:
			df1=pd.read_csv(filename1)
			df2=pd.read_csv(filename2)
	except Exception:
		error_type, error_instance, traceback = sys.exc_info()
		raise error_type, error_instance, traceback

def clean_data(df1,df2):
	""" This function is used to clean the data in dataframes 1 and 2 """
	try:
		''' finding duplicate id and replacing it with unique alphanumeric code
		  to maintain consistence and to join with other data frame '''
		df1.loc[df1.duplicated(['id']),'id']='4903x34'

		''' merging df1 and df2 dataframes and creating a new one '''
		new_df=pd.merge(df1, df2, on='id', how='outer')
		
		''' assigning 1 (female) to Sandrine after merging dataframes '''
		new_df.loc[new_df.first_name=='Sandrine',['sex']]='1'
		
		''' renaming columns as per API documentation '''
		new_df.rename(index=str,\
			columns={"attr2":"phone_numbers","id":"external_id","sex":"gender","tier":"custom_1",\
			"lastcontact":"custom_2"},inplace=True)

		''' tranlating 0 and 1 to Male and Female '''
		new_df['gender'] = np.where(new_df['gender'] ==0, 'm', 'f')

		''' dropping the below columns which are not required:
			# attr1_x from customer1.csv -- not making any sense 
			# engagement from customer1.csv -- not making any sense
			# pets from customer2.csv -- not making any sense
			# vehcle from customer2.csv -- not making any sense 
		'''
		new_df.drop(['attr1_x','engagement','pets','attr1_y'],inplace=True,axis =1)

		''' removing spaces from email id column '''
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
		new_df['opted_in'],new_df['external_id_type'],new_df['locale'],\
		new_df['ip'],new_df['dob'],new_df['address'],new_df['city'],\
		new_df['state'],new_df['zip'],new_df['country'],new_df['referral'],\
		new_df['phone_type']=[True,np.nan,'en-u',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'USA',np.nan,np.nan]

		''' correcting the date format present in custom_2 column '''
		new_df['custom_2'] = pd.to_datetime(new_df['custom_2']).dt.strftime('%Y-%m-%d')


		''' removing NaT from custom_2 field '''
		new_df['custom_2'] =  new_df['custom_2'].astype(str)
		new_df['custom_2'] = new_df['custom_2'].apply(lambda val : np.nan if val=="NaT" else val)

		''' arranging the columns in the order mentioned in API documentation '''
		new_df=new_df[['external_id','opted_in','external_id_type',\
		'email','locale','ip','dob','address','city','state','zip','country',\
		'gender','first_name','last_name','referral','phone_numbers','phone_type','custom_1','custom_2']]

	except Exception:
		error_type, error_instance, traceback = sys.exc_info()
		raise error_type, error_instance, traceback


def export_csv(new_df):
	''' Exporting data in CSV '''
	new_df.to_csv('Combined_Customer_data.csv')



def main():
	''' creating arg parse for reading inputs from command line '''
	parser = argparse.ArgumentParser()
	parser.parse_args()






if __name__=='__main__()':
	main()



