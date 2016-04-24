#
# import MySQLdb
# from yahoo_finance import Share
# from datetime import datetime,date,timedelta
# import time;
# import csv;
# import msvcrt;
# import webFinalIndicator
#
# class RunProgram(object):
# 	def __init__(self):
# 		'''
# 		self.indicator = webFinalIndicator.indicator();
# 		'''
# 		self.company_name = ["YHOO","GOOG","FB","AMZN","MSFT"];
# 		self.openTime = datetime.now().replace(hour = 9, minute = 30, second = 0);
# 		self.closeTime = datetime.now().replace(hour = 16, minute = 0, second = 0);
# 		self.createTable();
# 		self.initializeComppany();
# 		self.initializeOneYear();
# 		self.getData();
# 	def getOneyearData(self):
# 		return self.oneYearData_x, self.oneYearData_y;
# 	def getOnedayData(self):
# 		return self.oneDayData_x, self.oneDayData_y;
# 	def sqlImplement(self, sql):
# 		try:
# 			self.cursor.execute(sql)
# 			self.db.commit()
# 		except:
# 			self.db.rollback()
# 	def createTable(self):
# 		self.db = MySQLself.db.connect("localhost","root","921020");
# 		self.cursor = self.db.cursor();
# 		sql = "create database if not exists Stock"
# 		self.cursor.execute(sql);
# 		self.cursor.execute("use Stock");
# 		sql = "create table if not exists Company\
# 				(name varchar(10) not null,\
# 				primary key(name))"
# 		self.cursor.execute(sql);
# 		sql = "create table if not exists oneYearStock\
# 				(name varchar(10) not null, \
# 				time Date not null,\
# 				open double not null,\
# 				close double not null, \
# 				high double not null,\
# 				low double not null,\
# 				volume double not null,\
# 				primary key(name,time),\
# 				foreign key(name) references Company(name))"
# 		self.cursor.execute(sql);
# 		sql = "create table if not exists oneDayStock\
# 				(name varchar(10) not null,\
# 				time DateTime not null,\
# 				price double not null,\
# 				volume double not null,\
# 				primary key(name,time),\
# 				foreign key(name) references Company(name))"
# 		self.cursor.execute(sql);
# 		print ("finish create table");
#
# 	def initializeComppany(self):
# 		for name in company_name:
# 			sql = "select * from Company\
# 				where name = '%s'" % (name);
# 			result = self.cursor.execute(sql);
# 			if(result == 0):
# 				sql = "insert into Company(name) values('%s')" %(name);
# 				sqlImplement(sql, self.cursor, self.db);
# 		print ("finish initialize company table");
#
# 	def initializeOneYear(self):
# 		self.oneYearData_x = self.oneYearData_y = [];
# 		self.today = date.today() - timedelta(days = 1);
# 		self.oneYearBefore = self.today - timedelta(days = 365);
# 		for name in company_name:
# 			oneYearList = [];
# 			stock = Share(name);
# 			result = stock.get_historical(str(self.oneYearBefore),str(self.today));
# 			for ret in result:
# 				name = ret['Symbol']
# 				day = ret['Date']
# 				if name == 'MSFT':
# 					self.oneYearData_x.append(day);
# 				sql = "select * from oneYearStock\
# 						where name = '%s' and time = '%s'" %(name,day)
# 				reaction = self.cursor.execute(sql)
# 				if reaction == 0:
# 					Open = ret['Open']
# 					Close = ret['Close']
# 					Volume = ret["Volume"]
# 					High = ret["High"]
# 					Low = ret['Low']
# 					sql = "insert into oneYearStock(name,time,open,close,high,low,volume) values('%s','%s','%s','%s','%s','%s','%s')" %(name,day,Open,Close,High,Low,Volume)
# 					sqlImplement(sql, self.cursor, self.db);
# 					oneYearList.append(Close);
# 			#draw the previous year's rsi and sma
# 			self.oneYearData_y.append(oneYearList);
# 		self.outputOneYearCSV();
# 		print ("finish initialize  oneYearStock table");
# 	def outputOneYearCSV(self):
# 		for name in company_name:
# 			tmp = ('oneYearStock_%s' +'.csv') %(name);
# 			oneYearStock = file(tmp, 'wb');
# 			writer = csv.writer(oneYearStock, dialect = 'excel');
# 			writer.writerow(['name', 'time', 'open_price', 'close_price', 'dailyHigh', 'dailyLow', 'volume']);
# 			sql = "select * from oneYearStock where name = '%s'" %(name);
# 			self.cursor.execute(sql);
# 			res = self.cursor.fetchall();
# 			for row in res:
# 				writer.writerow(row);
# 			oneYearStock.close();
# 	def outputOneDayCSV(self):
# 		print ("click y to ouput tillself.now csv in 10 sec, if not continue running program");
# 		start_time = time.time();
# 		while 1:
# 			while msvcrt.kbhit():
# 				msvcrt.getch();
# 			if msvcrt.kbhit():
# 				key = ord(msvcrt.getche());
# 				if key in map(ord, 'yY'):
# 					print ('');
# 					print ("start generate onedaystock file");
# 					for name in self.company_name:
# 						tmp = ('oneDayStock_%s' +'.csv') %(name);
# 						oneDayStock = file(tmp, 'wb');
# 						writer = csv.writer(oneDayStock, dialect = 'excel');
# 						writer.writerow(['name', 'time', 'price', 'volume']);
# 						sql = "select * from oneDayStock where name = '%s'" %(str(name));
# 						self.cursor.execute(sql);
# 						res = self.cursor.fetchall();
# 						for row in res:
# 							writer.writerow(row);
# 						oneDayStock.close();
# 				if time.time() - start_time < 10:
# 					time.sleep(10-(time.time() - start_time));
# 					break;
# 			elif time.time() - start_time > 10:
# 				break;
# 		print ("go on programming");
# 	def getData(self):
# 		print ("program start");
# 		self.now  = datetime.now() - timedelta(minutes = 1);
# 		stop = False;
# 		self.oneDayData_x = [];
# 		self.oneDayData_y = [[] for i in range(len(self.company_name))];
# 		while True:
# 			if self.openTime < datetime.now() <= self.closeTime and datetime.now().minute != self.now.minute:
# 				self.now = datetime.now()
# 				self.oneDayData_x.append(self.now);
# 				i = 0;
# 				for name in self.company_name:
# 					stock = Share(name)
# 					price = stock.get_price()
# 					volume = stock.get_volume()
# 					sql = "insert into oneDayStock(name,time,price,volume) values('%s','%s','%s','%s')" % (str(name),str(self.now),str(price),str(volume))
# 					sqlImplement(sql, self.cursor, self.db);
# 					self.oneDayData_y[i].append(price);
# 					i += 1;
# 					'''
# 					self.indicator.sma(oneDayData_y);
# 					self.indicator.rsi(oneDayData_y);
# 					'''
# 				self.outputOneDayCSV();
# 				time.sleep(50);
# 			if datetime.self.now().hour > 16:
# 				self.oneDayData_x = [];
# 				self.oneDayData_y = [[] for i in range(len(self.company_name))];
# 				sql = "truncate table oneDayStock";
# 				sqlImplement(sql, self.cursor, self.db);
# 				while self.today == date.today();
# 				self.today = date.today();
# 				for name in company_name:
# 					sql = "delete from oneYearStock where time = '%s'" %self.oneYearBefore;
# 					sqlImplement(sql, self.cursor, self.db);
# 					stock = Share(name);
# 					Open = stock.get_open();
# 					Volume = stock.get_volume();
# 					High = stock.get_days_high();
# 					Low = stock.get_days_low();
# 					Close = stock.get_prev_close();
# 					self.oneYearData_y[i].append(Close);
# 					self.oneYearData_x[i].append(self.today);
# 					self.oneYearData_y[i] = self.oneYearData_y[i][1:];
# 					self.oneYearData_x[i] = self.oneYearData_x[i][1:];
# 					sql = "insert into oneYearStock(name,time,open,close,high,low,volume) values('%s','%s','%s','%s','%s','%s','%s')" %(str(name),str(self.today),str(Open),str(Close),str(High),str(Low),str(Volume));
# 					sqlImplement(sql, self.cursor, self.db);
# 				self.oneYearBefore = self.today - timedelta(days = 365);
#
# if __init__ == '__main__':
# 	run = RunProgram();
# 	'''
# 	yearX, yearY = run.getOneyearData();
# 	dayX, dayY
# 	'''
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# '''
# 			print ("give u 10 sec to click y to jummp out of the program");
# 			start_time = time.time();
# 			while 1:
# 				while msvcrt.kbhit():
# 					msvcrt.getch();
# 				if msvcrt.kbhit():
# 					key = ord(msvcrt.getche());
# 					if key in map(ord, 'yY'):
# 						print ('');
# 						print ('jump out of program');
# 						stop = True;
# 						break;
# 				elif time.time() - start_time >10:
# 					break;
# 			if stop:
# 				break;
# 			print ("go on");
#
#
#
# #sql = "select * from oneYearStock into outfile 'E:\\oneYearStock.txt\
# #		fields terminated by ',' enclosed by '""'\
# #		lines terminated by '\r\n'";
# #sqlImplement(sql, self.cursor);
# #sql = "select * from oneDyaStock into outfile 'E:\\oneDyaStock.txt\
# #		fields terminated by ',' enclosed by '""'\
# #		lines terminated by '\r\n'";
# #sqlImplement(sql, self.cursor);
#
# if flag:
# 	for name in company_name:
# 		tmp = ('oneDayStock_%s' +'.csv') %(name);
# 		oneDayStock = file(tmp, 'wb');
# 		writer = csv.writer(oneDayStock, dialect = 'excel');
# 		writer.writerow(['name', 'time', 'price', 'volume']);
# 		sql = "select * from oneDayStock where name = '%s'" %(str(name));
# 		self.cursor.execute(sql);
# 		res = self.cursor.fetchall();
# 		for row in res:
# 			writer.writerow(row);
# 		oneDayStock.close();
#
# print ('finish');
# self.db.close();
# '''