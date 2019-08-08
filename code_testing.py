import unittest
import pandas as pd
import sys
import csv

filename1=sys.argv[1]
filename2=sys.argv[2]

class TestSessionmDataGenProcess(unittest.TestCase):
	''' This class is implemented to run unit test cases to check 
		dataframe row/column count vs csv row/column counts '''

	def row_count_chk(self):
		''' This method is used to check row count in the file vs row count in dataframe '''
		try:
			filenames=[]
			filenames.extend((filename1,filename2))
			for i in filenames:
				with open(i,"r") as f:
					next(f)
					reader=csv.reader(f,delimiter=",")
					data=list(reader)
					row_count=len(data)
				df=pd.read_csv(i)
				df_row_count=df.shape[0]
				print(f'\nChecking row count of file vs row count of dataframe for file {i}')
				print(80*'-')
				print('Row Count from file:',row_count,'\t\tRow Count from dataframe:',df_row_count)
				self.assertEqual(row_count,df_row_count)
				print('\nUnit Test Passed OK\n')
		except AssertionError:
			print('\nUnit Test Failed !!\n')


	def col_count_chk(self):
		''' This method is used to check column count in the file vs column count in dataframe '''
		try:
			filenames=[]
			filenames.extend((filename1,filename2))
			for i in filenames:
				with open(i,"r") as f:
					next(f)
					reader=csv.reader(f,delimiter=",",skipinitialspace=True)
					first_row=next(reader)
					col_count=len(first_row)
				df=pd.read_csv(i)
				df_col_count=df.shape[1]
				print(f'\nChecking column count of file vs column count of dataframe for file {i}')
				print(80*'-')
				print('Column Count from file:',col_count,'\t\tColumn Count from dataframe:',df_col_count)
				self.assertEqual(col_count,df_col_count)
				print('\nUnit Test Passed OK\n')
		except AssertionError:
			print('\nUnit Test Failed !!\n')


if __name__=="__main__":
	obj=TestSessionmDataGenProcess()
	obj.row_count_chk()
	obj.col_count_chk()