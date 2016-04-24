# import numpy as np;
# import MySQLdb
# from numpy import convolve
# class indicator(object):
# #	def __init__(self):
# 	def sma(self, values, window = 3):
# 		weights = np.repeat(1.0, window)/window;
# 		sma = np.convolve(values, weights, 'valid');
# 		return sma;
# 	def rsi(self, prices, n = 14):
# 		deltas = np.diff(prices);
# 		seed = deltas[ : n+1];
# 		up = seed[seed >= 0].sum() / n;
# 		down = seed[seed < 0].sum() / n;
# 		rs = up / down;
# 		rsi = np.zeros_like(prices);
# 		rsi[ : n] = 100. - 100. / (1 + rs);
#
# 		for i in range(n, len(prices)):
# 			delta = deltas[i - 1];
# 			if delta > 0:
# 				upval = delta;
# 				downval = 0.;
# 			else :
# 				upval = 0.;
# 				downval = -delta;
# 			up = (up*(n - 1) + upval)/n;
# 			down = (down*(n - 1) + downval)/n;
# 			rs = up/down;
# 			rsi[i] = 100. - 100./(1. + rs);
# 		return rsi;
# '''
# a=[];
# b=[[],[]];
# b[1].append(1);
# print now.minute();
#
# db = MySQLdb.connect("localhost","root","921020");
# cursor = db.cursor();
# cursor.execute("use Stock");
# tmp = indicator();
# #company_name = ["YHOO","GOOG","FB","AMZN","MSFT"];
# company_name = "YHOO"
# sql = "select price from oneDayStock where name = '%s'" %(str(company_name));
# cursor.execute(sql);
# res = cursor.fetchall();
# print res;
# print type(res);
# aaa=list(res);
# print aaa;
# lista =[];
# for row in res:
# 	lista.append(row[0]);
#
# print lista;
# x=np.array([34.83, 34.64, 34.83, 34.5475, 34.83,34.73]);
# m= tmp.rsi(lista);
# print m;
#
# am= tmp.rsi(aaa);
# print am;
# t=tmp.sma(lista, 3);
# print t;
# print type(t);
# '''