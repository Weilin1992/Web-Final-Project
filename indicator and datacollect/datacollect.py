import MySQLdb
from yahoo_finance import Share
from datetime import datetime,date,timedelta
import time;
#import csv;
#import msvcrt;


class RunProgram(object):
	def __init__(self):
		self.company_name = ["YHOO","GOOG","FB","AMZN","MSFT", "BAC", "AAPL", "V","BX","BA"];
		self.openTime = datetime.now().replace(hour = 9, minute = 30, second = 0);
		self.closeTime = datetime.now().replace(hour = 16, minute = 0, second = 0);
		self.createTable();
		self.initializeComppany();
		self.initializeOneYear();
		self.getData();
	def sqlImplement(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()
	def createTable(self):
		self.db = MySQLdb.connect("localhost","root","1111");
		self.cursor = self.db.cursor();
		sql = "create database if not exists Stock"
		self.cursor.execute(sql);
		self.cursor.execute("use Stock");
		sql = "create table if not exists stockPrediction_Company\
				(id MEDIUMINT NOT NULL AUTO_INCREMENT,\
				name varchar(10) not null,\
				primary key(id))"
		self.cursor.execute(sql);
		sql = "create table if not exists stockPrediction_oneYearStock\
				(id MEDIUMINT NOT NULL AUTO_INCREMENT,\
				name varchar(10) not null, \
				time Date not null,\
				open double not null,\
				close double not null, \
				high double not null,\
				low double not null,\
				volume double not null,\
				primary key(id))"
		self.cursor.execute(sql);
		sql = "create table if not exists stockPrediction_oneDayStock\
				(id MEDIUMINT NOT NULL AUTO_INCREMENT,\
				name varchar(10) not null,\
				time DateTime not null,\
				price double not null,\
				volume double not null,\
				primary key(id))"
		self.cursor.execute(sql);
		print ("finish create table");

	def initializeComppany(self):
		for name in self.company_name:
			sql = "select * from stockPrediction_Company\
				where name = '%s'" % (name);
			result = self.cursor.execute(sql);
			if(result == 0):
				sql = "insert into stockPrediction_Company(name) values('%s')" %(name);
				self.sqlImplement(sql);
		print ("finish initialize stockPrediction_Company table");

	def initializeOneYear(self):
		self.today = date.today() - timedelta(days = 1);
		self.oneYearBefore = self.today - timedelta(days = 365);
		for name in self.company_name:
			stock = Share(name);
			result = stock.get_historical(str(self.oneYearBefore),str(self.today));
			for ret in result:
				name = ret['Symbol']
				day = ret['Date']
				sql = "select * from stockPrediction_oneYearStock\
						where name = '%s' and time = '%s'" %(name,day)
				reaction = self.cursor.execute(sql)
				if reaction == 0:
					Open = ret['Open']
					Close = ret['Close']
					Volume = ret["Volume"]
					High = ret["High"]
					Low = ret['Low']
					sql = "insert into stockPrediction_oneYearStock(name,time,open,close,high,low,volume) values('%s','%s','%s','%s','%s','%s','%s')" %(name,day,Open,Close,High,Low,Volume)
					self.sqlImplement(sql);
			#draw the previous year's rsi and sma
		print ("finish initialize  stockPrediction_oneYearStock table");
	def getData(self):
		print ("program start");
		self.now  = datetime.now() - timedelta(minutes = 1);
		while True:
			if self.openTime < datetime.now() <= self.closeTime and datetime.now().minute != self.now.minute:
				self.now = datetime.now()
				for name in self.company_name:
					stock = Share(name)
					price = stock.get_price()
					volume = stock.get_volume()
					sql = "insert into stockPrediction_oneDayStock(name,time,price,volume) values('%s','%s','%s','%s')" % (str(name),str(self.now),str(price),str(volume))
					self.sqlImplement(sql);
				time.sleep(50);
			if datetime.now().hour > 16:
				#print 'aa';
				sql = "truncate table stockPrediction_oneDayStock";
				self.sqlImplement(sql);
				while self.today == date.today():
					print ""
				self.today = date.today();
				for name in self.company_name:
					sql = "delete from stockPrediction_oneYearStock\
							where time = '%s' and name = '%s" %(self.oneYearBefore, name);
					self.sqlImplement(sql);
					stock = Share(name);
					Open = stock.get_open();
					Volume = stock.get_volume();
					High = stock.get_days_high();
					Low = stock.get_days_low();
					Close = stock.get_prev_close();
					sql = "insert into stockPrediction_oneYearStock(name,time,open,close,high,low,volume) values('%s','%s','%s','%s','%s','%s','%s')" %(str(name),str(self.today),str(Open),str(Close),str(High),str(Low),str(Volume));
					self.sqlImplement(sql);
				self.oneYearBefore = self.today - timedelta(days = 365);
run = RunProgram();
























'''
			print ("give u 10 sec to click y to jummp out of the program");
			start_time = time.time();
			while 1:
				while msvcrt.kbhit():
					msvcrt.getch();
				if msvcrt.kbhit():
					key = ord(msvcrt.getche());
					if key in map(ord, 'yY'):
						print ('');
						print ('jump out of program');
						stop = True;
						break;
				elif time.time() - start_time >10:
					break;
			if stop:
				break;
			print ("go on");



#sql = "select * from stockPrediction_oneYearStock into outfile 'E:\\stockPrediction_oneYearStock.txt\
#		fields terminated by ',' enclosed by '""'\
#		lines terminated by '\r\n'";
#sqlImplement(sql, self.cursor);
#sql = "select * from oneDyaStock into outfile 'E:\\oneDyaStock.txt\
#		fields terminated by ',' enclosed by '""'\
#		lines terminated by '\r\n'";
#sqlImplement(sql, self.cursor);

if flag:
	for name in company_name:
		tmp = ('stockPrediction_oneDayStock_%s' +'.csv') %(name);
		stockPrediction_oneDayStock = file(tmp, 'wb');
		writer = csv.writer(stockPrediction_oneDayStock, dialect = 'excel');
		writer.writerow(['name', 'time', 'price', 'volume']);
		sql = "select * from stockPrediction_oneDayStock where name = '%s'" %(str(name));
		self.cursor.execute(sql);
		res = self.cursor.fetchall();
		for row in res:
			writer.writerow(row);
		stockPrediction_oneDayStock.close();

print ('finish');
self.db.close();
'''
