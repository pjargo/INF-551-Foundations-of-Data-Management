from django.shortcuts import render
import pyrebase
from firebase import firebase
import json
from . import database_specs
from django.contrib import auth
from django.http import HttpResponse
firebaseurl = 'https://inf-551-final-project.firebaseio.com/'
import requests
# configure firebase for retrieval (remove when app in place)
config = {
    "apiKey": "AIzaSyCZn49b_Pz53gUO34TFjg1Yg654MvxK9XY",
    "authDomain": "inf-551-final-project.firebaseapp.com",
    "databaseURL": "https://inf-551-final-project.firebaseio.com",
    "projectId": "inf-551-final-project",
    "storageBucket": "inf-551-final-project.appspot.com",
    "messagingSenderId": "1039547012860",
    "appId": "1:1039547012860:web:4d1ad94d80b1935a9da979",
    "measurementId": "G-GW9M8Y34R6"
}
firebase = pyrebase.initialize_app(config);
# firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
print(authe)
# database=firebase.database()
def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    # print(user['idToken'])
    # session_id=user['idToken']
    # request.session['uid']=str(session_id)
    return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signUp(request):
    return render(request,"signUp.html")
#create an account:
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passwd=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passwd)
    except:
        message="At least 6 charactors for password"
        return render(request,"signUp.html",{"messg":message})
    return render(request,'signIn.html')

def post_results(request):
    lookup = request.GET.get('z')
    my_key = request.GET.get('y')    
    my_db = request.GET.get('x')
    #for the world database:
    reverse_relationship = {}
    if my_db == 'world':
        reverse_relationship['CountryCode'] = ['country']
        reverse_relationship['Code'] = ['city','countrylanguage']
    if  my_db == 'employees':
        reverse_relationship['emp_no'] = ['employees']
    if  my_db == 'sakila':
        reverse_relationship['language_id'] = ['language']
        reverse_relationship['film_id'] = ['film_actor']
        reverse_relationship['actor_id'] = ['film_actor']



    if my_db == 'world':
        pkeys_dictionary = ['Code','ID','CountryCode']
    elif my_db == 'employees':
        pkeys_dictionary = ['dept_no','emp_no']
    elif my_db == 'sakila':
        pkeys_dictionary = ['film_id','actor_id','language_id']

    children = reverse_relationship[my_key]

    for child in children:
        print(my_db, child, lookup)
        if child == 'country':
            response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{lookup.upper()}'+'.json').json() 
        elif child == 'countrylanguage':
            response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{lookup.upper()}'+'.json').json() 
            # https://inf-551-final-project.firebaseio.com/world_countrylanguage/ABW
        else:
            response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{lookup}'+'.json').json()
    if type(response) == dict:
        response = [response]


    return render(request,'post_results.html',{'result':response, 'lookup': lookup, 'key':my_key,'keys': pkeys_dictionary,'Database': my_db})

def getdata(request):
    keywords=request.GET.get('search')
    keywords=keywords.split(' ')
    my_db = request.GET.get('Database')
    print(f'my database selected is {my_db}')
    print(keywords)
    if my_db == 'world':
        pkeys_dictionary = ['Code','CountryCode']
    elif my_db == 'employees':
        pkeys_dictionary = ['dept_no','emp_no']
    elif my_db == 'sakila':
        pkeys_dictionary = ['film_id','actor_id','language_id']
    
    word_list = []
    responses = []
    if len(keywords) == 1:
        keyword = keywords[0].lower()
        response=requests.get(f'https://inf-551-final-project.firebaseio.com/index_{my_db}/{keyword}'+'.json').json() 
        if  response is None:
            print(response)
            results = response
            return render(request,'results.html',{'result':results, 'keyword':keywords[0]})
            
        sorted_responses = []
        for elem in response:
            sorted_responses.append(elem)


    else:
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword not in word_list: #remove duplicates
                word_list.append(keyword)
        for word in word_list:
            response = requests.get(f'https://inf-551-final-project.firebaseio.com/index_{my_db}/{word}'+'.json').json()
            if response is None:
                pass
            else:
                responses.append(response)
            # print(requests.get(f'https://inf-551-final-project.firebaseio.com/index_{database}/{word}'+'.json'))

        # get two lists, one list of all elements, one of unique elements only
        temp = [] # list of uniqe elements
        temp2 = [] #list of all elementer
        for response in responses:
            for elem in response:
                temp2.append(elem)
                if elem not in temp:
                    temp.append(elem)
        
        #count the frequency of each element and return a tuple of each element with its count
        count_list = []
        for elem in temp:
            i = 0
            for elem2 in temp2:
                if elem == elem2:
                    i += 1
            count_list.append((elem,i))

        # Sort the list of tuples in descending order to rank the results
        sort_t = sorted(count_list, key = lambda x: x[1],reverse = True)

        # extract the response value from the sorted tuple list
        sorted_responses = []
        for elem in sort_t:
            sorted_responses.append(elem[0])

    results = []   
    for item in sorted_responses:
        print(item)
        print(type(item))
        child = item['TABLE'] # {'COLUMN': 'Name', 'ID': '1035', 'TABLE': 'city'}
        try:
            primary_keys = database_specs.db_specs[my_db]['tables'][child]['primarykeys'] #There might need to be multiple primarykeys if a table has multiple instances of the inverted index
            # ex. {Table: titles, column: title, Row: 10004}
            # [language, countrycode] ----> {'COLUMN': 'Language', 'CountryCode': 'vir', 'TABLE': 'countrylanguage'}
        except:
            continue
        if len(primary_keys) == 1:
            pkey = primary_keys[0]
            query = item[pkey] 
            if child == 'country':
                response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{query.upper()}'+'.json').json() 
            else:
                response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{query}'+'.json').json()
            results.append(response)
        
        else:
            
            language_key = primary_keys[0] #language
            countrycode_key = primary_keys[1] #countrycode

            query_val_a= item[countrycode_key] 
            query_val_b  = keywords[0]
            if child == 'country':
                response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{query_val_a.upper()}'+'.json').json() 
            elif child == 'countrylanguage':
                response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{query_val_a.upper()}'+'.json').json() 
                # https://inf-551-final-project.firebaseio.com/world_countrylanguage/ABW
            else:
                response=requests.get(f'https://inf-551-final-project.firebaseio.com/{my_db}_{child}/{query_val_a}'+'.json').json()
            
            # print(response)
            if response is not None:
                if response[item['COLUMN']].lower() == query_val_b:
                    print(response)
                    results.append(response)


    final_results = [] # Remove duplicates
    for result in results:
        if result not in final_results:
            final_results.append(result)



    for result in results:
        print(result)
    return render(request,'results.html',{'result':final_results, 'Database': my_db, 'keys': pkeys_dictionary})

