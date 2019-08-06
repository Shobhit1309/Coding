SessionM Data Generation Process
-----------------------------------
  
Assumptions for Customer1.csv:
##############################
 
 1) id 4903g34 is duplicate which is an identifier for customer in external system but there are 2 rows with the same id with different data which might be because of some data corruption happened at the source system.
 
     Correction measure taken:
     -------------------------
     To correct this i have assigned a new alpha numeric id to user named Sandrine.This will help in identifying the records with the correct information and after joining both the data frames (customer1 and customer2) we'll be able to make correct assumptions and processing.
  
 2) There is space in the email address of jh41922 id i.e sam2382@mailinator .com. This might be an issue of wrong entry by the user in source system.To correct the data the spaces are trimmed.
 
 3) Attr1 is not showing any meaningful information related to customer. Hence this will be dropped from dataframe.
 
 4) Engagement is not present in SessionM API documentation and is not adding any insights to the data, hence will be dropped from the dataframe.
 
Assumptions for Customer2.csv:
##############################

 1) By looking at the data '0' under sex column means Male (m) and '1' means female (f).
 
 2) By looking at the data and sessionM api documentation 'tier' means the plans opted by customer.In this csv all the customers are opted-in for plans hence the value would be True under 'opted_in' column and details will be kept under custom_attr1.
 
 3) By looking at the data 'lastcontact' shows last time the customer was contacted or used any service.Since this field is not mentioned in the API documentation hence will be placed under custom_attr1.Keeping this field because it can be used if someone whats to get insights of data for the customers which are active recently.
 
    Correction measure taken:
    -------------------------
     The format of last contacted date is inconsistent. Hence converting all in YYYY-MM-DD format.
 
 4) By looking at the data under 'pets' column , 0 means no pets own by a customer and 1 means pets own by a customer. As per SessionM API documentation, there is no column related to 'pets' information and and is not adding any insights to the data,  hence dropping the column.
 
 5) By looking at the data 'attr1' shows the vehicle owned by a customer. Since this field is not mentioned in the API documentation and is not adding any insights to the data, hence dropping the column.
 
 6) By looking at the data 'attr2' shows the phone number of customers. This should be placed under phone number column. Also there is one more information which can be derived from phone number i.e country. +1 is a code for USA, which can be placed under country column.
 
 
Questions:
##########

 1) How the id 4903g34 is same for 2 records from the source. This should be a random generated number from source system. Can the same id be assigned to other user as well , or is there a concept of expiration account on the source system i.e. id of the account which is now expired can be assigned to other user?
 
 2) How come sam2382@mailinator .com with spaces in the email id column allowed in the source system. Is there no validation on email id field on source?
 
 3) What is the use of engagement,attr1 in customer1.csv and pets,attr1 in customer2.csv as no information is derived from these columns which can be used in other columns mentioned in API documentation?
