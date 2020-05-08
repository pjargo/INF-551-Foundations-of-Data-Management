# this file specifies all the databases in the search engine, and their characteristics such as column names, 
# primary and foreign keys, and the firebase urls where they're stored

# main dictionary that holds all the databases
db_specs={}

####### first database is the world database ########
world={}

# which has 3 tables:
country={}
columns=['code','name','continent','region','surfacearea','indepyear','population','lifeExpectancy','gnp','gnpold','localname','governmentForm','headofstate','capital','code2']
primarykeys=['Code']
foreignkeys=[]
country['columns']=columns
country['primarykeys']=primarykeys
country['foreignkeys']=foreignkeys

city={}
columns=['ID','name','CountryCode','district','population']
primarykeys=['ID']
foreignkeys=['CountryCode']
city['columns']=columns
city['primarykeys']=primarykeys
city['foreignkeys']=foreignkeys

countrylanguage={}
columns=['countrycode','language','isofficial','percentage']
primarykeys=['Language','CountryCode']
foreignkeys=['Countrycode']
countrylanguage['columns']=columns
countrylanguage['primarykeys']=primarykeys
countrylanguage['foreignkeys']=foreignkeys

# combine the three tables, and add to the world dictionary
tables={}
tables['country']=country
tables['city']=city
tables['countrylanguage']=countrylanguage
world['tables']=tables

# and lastly, add the firebase url
world['firebaseurl']='https://inf551-world-project.firebaseio.com'


####### second database is the employees database ########
employees={}

# 6 available tables
departments={}
columns=['dept_no','dept_name']
primarykeys=['dept_no']
foreignkeys=[]
departments['columns']=columns
departments['primarykeys']=primarykeys
departments['foreignkeys']=foreignkeys

dept_emp={}
columns=['emp_no','dept_no','from_date', 'to_date']
primarykeys=['emp_no']
foreignkeys=['emp_no','dept_no']
dept_emp['columns']=columns
dept_emp['primarykeys']=primarykeys
dept_emp['foreignkeys']=foreignkeys

dept_manager={}
columns=['emp_no', 'dept_no', 'from_date', 'to_date']
primarykeys=['emp_no']
foreignkeys=['emp_no','dept_no']
dept_manager['columns']=columns
dept_manager['primarykeys']=primarykeys
dept_manager['foreignkeys']=foreignkeys

employees={} #problem with table and database having the same name 
columns=['emp_no', 'birth_date', 'first_name', 'last_name','gender','hire_date']
primarykeys=['emp_no']
foreignkeys=[]
employees['columns']=columns
employees['primarykeys']=primarykeys
employees['foreignkeys']=foreignkeys

salaries={}
columns=['emp_no', 'salary', 'from_date', 'to_date']
primarykeys=['emp_no']
foreignkeys=['emp_no']
salaries['columns']=columns
salaries['primarykeys']=primarykeys
salaries['foreignkeys']=foreignkeys

titles={}
columns=['emp_no', 'title', 'from_date', 'to_date']
primarykeys=['emp_no']
foreignkeys=['emp_no']
titles['columns']=columns
titles['primarykeys']=primarykeys
titles['foreignkeys']=foreignkeys


tables={}
tables['departments']=departments
tables['dept_emp']=dept_emp
tables['dept_manager']=dept_manager
tables['employees']=employees
tables['salaries']=salaries
tables['titles']=titles
employees['tables']=tables

############################################### SAKILA #############################################
sakila={}

actor={}
columns=['actor_id', 'first_name', 'last_name', 'last_update']
primarykeys=['actor_id']
foreignkeys=['']
actor['columns']=columns
actor['primarykeys']=primarykeys
actor['foreignkeys']=foreignkeys

film={}
columns=['film_id', 'title', 'description', 'release_year', 'language_id', 'original_language', 'rental_duration', 'rental_rate', 'length', 'replacement_cost', 'rating', 'special_features', 'last_update']
primarykeys=['film_id']
foreignkeys=['language_id']
film['columns']=columns
film['primarykeys']=primarykeys
film['foreignkeys']=foreignkeys

film_actor={}
columns=['actor_id', 'film_id', 'last_update']
primarykeys=['actor_id', 'film_id']
foreignkeys=['actor_id','film_id']
film_actor['columns']=columns
film_actor['primarykeys']=primarykeys
film_actor['foreignkeys']=foreignkeys

language={}
columns=['language_id', 'name', 'last_update']
primarykeys=['language_id']
foreignkeys=[]
language['columns']=columns
language['primarykeys']=primarykeys
language['foreignkeys']=foreignkeys

tables={}
tables['actor']=actor
tables['film']=film
tables['film_actor']=film_actor
tables['language']=language
sakila['tables']=tables

db_specs['world']=world
db_specs['employees']=employees
db_specs['sakila']=sakila


