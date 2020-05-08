# Read the mysql database 
# Put the coloumn bnames into their own list
import os
import mysql.connector
import json
import requests
import re
from firebase import firebase
#Read the MySQL database. Update the database name with the relevant database
class SQL_to_firebase:
    def __init__(self, database, firebase_path):
        self.db = database
        
        self.mydb = mysql.connector.connect(host="127.0.0.1",user="root",password='Yankees2009!',
                               database=self.db,auth_plugin='mysql_native_password')
        
        self.firebase_path = firebase_path
        self.firbase_file = firbase_file
        
        # Problem: The pkeys help deermine the row for the index. Index specifies Table, column, and row. However this is only a unique combination if the row contains a primaryu key
        # I need to include all elemnts that would make the row unique, even if that icludes multiple keys
        if self.db == 'world': 
            self.pkeys = ['Code', 'ID', 'ID']
            self.pkeys_dictionary = {'country':'Code','city':'ID','countrylanguage':'CountryCode'}
        elif self.db == 'employees':
            self.pkeys_dictionary = {'departments':'dept_no',    'dept_emp':'dept_no',     'dept_manager':'emp_no',            'employees':'emp_no',      'salaries':'emp_no',     'titles':'emp_no'}

        self.inv_index = {}# The inverted index should be should be instantiated here and continued to be added to for all tables in the the database

        self.get_tables()
        self.counter = 1
        for table in self.my_tables:
            # if table == 'titles': # remove this, this is for trouble shooting
            self.table = table
            self.get_mysql()
            self.mysql_2_json()
            # self.json_2_firebase()
            self.build_inv_index()
            self.counter += 1


    def get_tables(self):
        self.mycursor = self.mydb.cursor() #Create my cursor 
        sql = "SHOW TABLES;"

        #  Execute the SQL query and get the response
        self.mycursor.execute(sql)
        tables = self.mycursor.fetchall()
        self.my_tables = []
        for row in tables:
            self.table = row[0] # this should be removed once we figure out how to iterate through all the tables
            print(row[0])
            self.my_tables.append(row[0])  
        
    def get_mysql(self):
        self.mycursor = self.mydb.cursor() #Create my cursor 

        self.sql = f"SELECT * FROM {self.table}"
        self.mycursor.execute(self.sql)
        self.myresult = self.mycursor.fetchall() #get all the contents of the table

        self.column_headers = []
        self.table_contents = []

        # Get the column names for the table
        self.num_fields = len(self.mycursor.description)
        self.field_names = [i[0] for i in self.mycursor.description]

        for row in self.myresult:
            self.table_contents.append([str(item) for item in row])
            

    def mysql_2_json(self):
        self.row_dictionary_list = []
        self.row_dictionary_object = {}
        for row in self.table_contents:
            self.row_dictionary = {}
            self.temp_dict = {}
            for i in range(len(row)):
                if i == 0:
                    self.primary_key = row[i]
                self.key = self.field_names[i]
                self.value = row[i]
                self.temp_dict[self.key] = self.value
                if i == len(row)-1:
                    self.row_dictionary[self.primary_key] = self.temp_dict
                    self.row_dictionary_object[self.primary_key] = self.temp_dict
        #             print(temp_dict)
            self.row_dictionary_list.append(self.row_dictionary)
        # print(self.field_names)
        # print(self.table_contents)
        # print("\n")
        
        # print(self.row_dictionary_object)
        # print("\n")
        # print(self.row_dictionary_list)
        
    def json_2_firebase(self):
        filename =f'C:\\Users\\Peter\\Desktop\\Classes\\INF 551\\Project\\Final_Project\\{self.db}_{self.table}.json' 
        with open(filename, "w") as jsonFile:
            jsonFile.write(json.dumps(self.row_dictionary_object, indent = 4))
        
        self.firebase_path = f'https://inf-551-final-project.firebaseio.com/{self.db}_{self.table}.json'
        self.response = requests.put(self.firebase_path, json.dumps(self.row_dictionary_object, indent = 4))
        print(self.response)

    def index_2_firebase(self):
        filename =f'C:\\Users\\Peter\\Desktop\\Classes\\INF 551\\Project\\Final_Project\\invert_{self.db}.json' 
        with open(filename, "w") as jsonFile:
            jsonFile.write(json.dumps(self.inv_index, indent = 4))
        
        self.firebase_path = f'https://inf-551-final-project.firebaseio.com/index_{self.db}.json'
        self.response = requests.put(self.firebase_path, json.dumps(self.inv_index, indent = 4))
        print(self.response)

    def build_inv_index(self):
        ''' configure the inverted indexs
        '''
        regex = re.compile('[^A-Za-z0-9 ]+')
        p_key = self.pkeys_dictionary[self.table]

        for row in self.row_dictionary_list:
            for key in row:
                my_key = key
                my_id = row[my_key][p_key]
                my_id = my_id.lower() #Convert to lowercase
                my_id = re.sub(r'[~`-]', '', my_id)
                my_id = regex.sub('', my_id)
                my_id = re.sub(r'\\', '', my_id)
                my_id = my_id.strip()
            
            row_cols = list(row[my_key].keys())
            for col in row_cols:
                val = row[my_key][col]

                #Evaluate the type of the value
                #Remove if the value is an integer
                if str(val).isdigit():
                    continue

                if  str(val[0:4]).isdigit(): #remove dates for the employees database
                    continue
                    
                #Remove if the value is a float
                if str(val).isnumeric():
                    continue 

               #Remove if the value is Null or length 0/1
                if val == 'NULL':
                    continue
                if len(val) == 0:
                    continue
                if len(val) ==1:
                    continue
                

                #STEP 2: Preprocess the string, before adding to index
                val_list = val.split(' ') #Split value in case the word length > 1

                for word in val_list:
                    word = word.lower() #Convert to lowercase
                    word = re.sub(r'[~`!@#$%^&*-_+=|?]', '', word)
                    word = re.sub(r'\\', '', word)
                    # word = regex.sub('', word)
                    if word == '': #Removes keys that are nothing ''
                        continue
                    if len(word) == 1:
                        continue
                    
                    # If the string value does not yet in self.inv_index, add it
                    if word not in self.inv_index:
                        self.inv_index[word] = [{'TABLE': self.table, 'COLUMN': col, p_key: my_id}]

                    # If the word already exists in dictionary, append to that word value list 
                    else:
                        self.inv_index[word].append({'TABLE': self.table, 'COLUMN': col, p_key: my_id})
        
        if self.counter == len(self.my_tables): 
            self.index_2_firebase()

        # if self.table = 'titles': #Remove this after trouble shooting 
        #     self.index_2_firebase()


database = "employees"
firebase_path = 'https://inf-551-final-project.firebaseio.com/employees.json'
firbase_file = 'employees.json'
X = SQL_to_firebase(database,firebase_path)

# for key in X.inv_index:
#     print(key, X.inv_index[key])
# print(len(X.inv_index))