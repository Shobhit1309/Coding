SessionM Data Generation Process
-----------------------------------
  
Assumptions for Customer1.csv:
##############################
 
1) id 4903g34 is duplicate which is an identifier for customer in external system but there are 2 rows with the same id with different data which might be because of some data corruption happened at the source system.

Correction measure taken:
-------------------------
To correct this I have assigned a new alpha numeric id to user named Sandrine.This will help in identifying the records with the correct information and after joining both the data frames (customer1 and customer2) we'll be able to make correct assumptions and processing.

2) There is space in the email address of jh41922 id i.e sam2382@mailinator .com. This might be an issue of wrong entry by the user in source system.To correct the data the spaces are trimmed.

3) Attr1 is not showing any meaningful information related to customer. Hence this will be dropped from dataframe.

4) Engagement is not present in SessionM API documentation and is not adding any insights to the data, hence will be dropped from the dataframe.
 
Assumptions for Customer2.csv:
##############################

1) By looking at the data '0' under sex column means Male (m) and '1' means female (f).

2) By looking at the data and sessionM api documentation 'tier' means the plans opted by customer.In this csv all the customers are opted-in for plans hence the value would be True under 'opted_in' column and details will be kept under custom_attr1.

3) By looking at the data 'lastcontact' shows last time the customer was contacted or used any service.Since this field is not mentioned in the API documentation hence will be placed under custom_attr2.Keeping this field because it can be used if someone whats to get insights of data for the customers which are active recently.
 
4) By looking at the data under 'pets' column , 0 means no pets own by a customer and 1 means pets own by a customer. As per SessionM API documentation, there is no column related to 'pets' information and and is not adding any insights to the data,  hence dropping the column.

5) By looking at the data 'attr1' shows the vehicle owned by a customer. Since this field is not mentioned in the API documentation and is not adding any insights to the data, hence dropping the column.

 
Questions:
##########

1) How the id 4903g34 is same for 2 records from the source. This should be a random generated number from source system. Can the same id be assigned to other user as well , or is there a concept of expiration account on the source system i.e. id of the account which is now expired can be assigned to other user?

2) How come sam2382@mailinator .com with spaces in the email id column allowed in the source system. Is there no validation on email id field on source?

3) What is the use of engagement,attr1 in customer1.csv and pets,attr1 in customer2.csv as no information is derived from these columns which can be used in other columns mentioned in API documentation?


++++++++++++++++++++++++++++++++++++++++
Program execution steps and prequisites:
++++++++++++++++++++++++++++++++++++++++

Prequisites:
=============
1) Latest Anaconda distribution must be installed.
2) Keep all the datafiles (customer1.csv and customer2.csv) in the same directory where python program file sessionm_data_generation.py is present.

Execution steps:
================
1) Run the below command line after navigating to the location where program file and data files are present.
python sessionm_data_generation.py --sourcefile1 "customer1.csv" --sourcefile2 "customer2.csv"

Also there is help and version options available to know more about the program file and the argument it accepts.
python sessionm_data_generation.py --help
python sessionm_data_generation.py --version

Output of program:
==================

--------------------------------- SessionM-Data-Generation-Program ---------------------------------

 Program started on: Aug 17 2019 18:33:19
 Loading datafiles into dataframe: DONE
 Cleaning data: DONE
 Running data sanity checks on cleaned data: DONE
 Exporting data into Combined_Customer_data.csv: DONE
 Process completed Successfully!
 Program ended on : Aug 17 2019 18:33:19

 ----------------------------------------------------------------------------------------------------
 
 Data Validation Checks in the program:
 =======================================
A function is used in the program to validate the cleaned data before writing it to csv. This will check the below: 
1) Emailids must be encrypted
2) Gender must be M or F
3) Opted_in must be true or false

Logging:
========
Logging feature is provided in the program , hence while execution the program creates log file and capture all the activities 
which are running inside a program.

Below is the sample of log file after successful completion of program:
-----------------------------------------------------------------------

2019-08-17 18:33:19,064:INFO:Input params
2019-08-17 18:33:19,064:INFO:--------------------------------------------------------------------------------
2019-08-17 18:33:19,064:INFO:Namespace(source_file1='customer1.csv', source_file2='customer2.csv')
2019-08-17 18:33:19,064:INFO:--------------------------------------------------------------------------------
2019-08-17 18:33:19,064:INFO:Calling load_csv function to read csv and create dataframes
2019-08-17 18:33:19,079:INFO:customer1.csv is loaded in df1 dataframe
2019-08-17 18:33:19,079:INFO:customer2.csv is loaded in df2 dataframe
2019-08-17 18:33:19,111:INFO:Calling clean_data function to clean data and create a new dataframe new_df
2019-08-17 18:33:19,111:INFO:Finding duplicate id and replacing it with unique alphanumeric code to maintain consistence and to join with other data frame
2019-08-17 18:33:19,111:INFO:Merging df1 and df2 dataframes and creating a new one
2019-08-17 18:33:19,127:INFO:Assigning 1 (female) to Sandrine after merging dataframes
2019-08-17 18:33:19,127:INFO:Renaming columns as per API documentation
2019-08-17 18:33:19,131:INFO:Tranlating 0 to Male 1 to Female and other codes to invalid gender
2019-08-17 18:33:19,131:INFO:Dropping the below columns which are not required:
			attr1_x from customer1.csv, engagement from customer1.csv, pets from customer2.csv, vehcle from customer2.csv
2019-08-17 18:33:19,131:INFO:Removing spaces from email id column
2019-08-17 18:33:19,131:INFO:Encrypting email ids
2019-08-17 18:33:19,226:INFO:Additing the below columns as per sessionM API documentation
			opted_in,external_id_type,locale,ip,dob,address,city,state,zip,country,referral,phone_type
2019-08-17 18:33:19,230:INFO:Correcting the date format present in custom_2 column
2019-08-17 18:33:19,230:INFO:Removing NaT from custom_2 field
2019-08-17 18:33:19,230:INFO:Arranging the columns in the order mentioned in API documentation
2019-08-17 18:33:19,230:INFO:Calling data_validator function to perform data sanity checks before exporting to csv file
2019-08-17 18:33:19,262:INFO:Calling export_data function to export the data in combined customer data csv file
2019-08-17 18:33:19,262:INFO:Exporting data in CSV: Combined_Customer_data.csv
2019-08-17 18:33:19,266:INFO:Data exported in CSV!
2019-08-17 18:33:19,266:INFO:Process completed Successfully!! Combined Customer data file generated.


========================================================
Unit Testing of Sessionm_data_generation.py program
========================================================

Python Unittest module is used to write unit test cases in order to perform basic unit testing of Sessionm_data_generation.py program. In Unittesting the below points are tested to ensure Sessionm_data_generation.py is working fine.
	a) Matching the no. of rows present in csv file vs no. of rows loaded in dataframe.
	b) Matching the no. of columns present in csv file vs no. of columns loaded in dataframe.
	
Below command line is used to execute the unit test case:
python code_testing.py "customer1.csv" "customer2.csv"

Note: Keep the datafiles and unit test program in the same directory.

Output of program:
------------------

Checking row count of file vs row count of dataframe for file customer1.csv
--------------------------------------------------------------------------------
Row Count from file: 4          Row Count from dataframe: 4

Unit Test Passed OK


Checking row count of file vs row count of dataframe for file customer2.csv
--------------------------------------------------------------------------------
Row Count from file: 4          Row Count from dataframe: 4

Unit Test Passed OK


Checking column count of file vs column count of dataframe for file customer1.csv
--------------------------------------------------------------------------------
Column Count from file: 6               Column Count from dataframe: 6

Unit Test Passed OK


Checking column count of file vs column count of dataframe for file customer2.csv
--------------------------------------------------------------------------------
Column Count from file: 7               Column Count from dataframe: 7

Unit Test Passed OK
