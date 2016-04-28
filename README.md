# Web-Final-Project



##0.setup:

	database setting:
		Final_Project/settings.py use your own database password and name
		DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.mysql',
        	'NAME': 'Stock',
        	'USER': 'root',
        	'PASSWORD': 'password',
        	'HOST': '127.0.0.1',
        	'PORT': '3306',
    		}
		}
	
	run:
	python manage.py makemigrations stockPrediction
	python manage.py migrate
	python manage.py runserver


##1.api: Django rest framework:
  
we use [django rest framework](http://www.django-rest-framework.org) to define api  
  
	(1) Show the list of all companies in the database along with their latest stock price.  
	http://127.0.0.1:8000/api/latestOneyearstock/  
	
	(2) Get the highest stock price of Google in the last ten days  
	http://127.0.0.1:8000/api/highestLastnDays/?name=GOOG&day=10    
	
	(3) Average stock price of Microsoft in the latest one year  
	http://127.0.0.1:8000/api/average/?name=YHOO  
	
	(4)Lowest stock price for each company in the latest one year  
	http://127.0.0.1:8000/api/lowest/  
	
	(5)indicators  
	http://127.0.0.1:8000/api/indicator/?name=YHOO&indicator=xxx&timescale=xxx  
	
	(6)daystockPrediction  
	http://127.0.0.1:8000/api/dayPrediction/?name=YHOO&strategy=xxx&days=5  
	
	(7)minstockPrediction  
	http://127.0.0.1:8000/api/minPrediction/?name=YHOO&strategy=xxx&minutes=5  

    (8)realtime query
    http://127.0.0.1:8000/api/realTime/?name=YHOO
    
    (9)onedaystock
    http://127.0.0.1:8000/api/onedaystock/?name=YHOO
    
    (10)oneyearstock
    http://127.0.0.1:8000/api/oneyearstock/?name=YHOO
    
##2.prediction api:  
in api/prediction:  

	daystockPrediction(company_name,strategy,days)
	
	minstockPrediction(company_name,strategy,minutes)
	
	indicatorCalculate(company_name, indicatorname, min_or_days)


##3.django database query:
	from django.db import connection
	company_name = 'YHOO'
	cursor = connection.cursor()
    cursor.execute('select * from stockPrediction_onedaystock where name = %s',[company_name])

##4.Database changes:
1.rename: add stockPrediction_ to each table  
2.remove foreign key for every table, add a primery key id = autoIncrement

	create table if not exists stockPrediction_company(id MEDIUMINT NOT NULL AUTO_INCREMENT,name varchar(10) not null, primary key(id))
	
	create table if not exists stockPrediction_oneyearstock(id MEDIUMINT NOT NULL AUTO_INCREMENT, name varchar(10) not null, time Date not null,open double not null,close double not null, high double not null,low double not null,volume double not null,primary key(id))
	
	create table if not exists stockPrediction_onedaystock(id MEDIUMINT NOT NULL AUTO_INCREMENT,name varchar(10) not null, time DateTime not null,price double not null,volume double not null,primary key(id))



  
  

	
