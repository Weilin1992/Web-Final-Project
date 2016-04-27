import MySQLdb
from sklearn import svm
from sklearn import neural_network
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import baycurve as bs
import numpy as np
import collections
from stockPrediction.models import *
from datetime import datetime,date,timedelta

from django.db import connection

def getSamples(name, attr, attr2 = 'volume',n = 60):
    cursor = connection.cursor()
    sql = 'SELECT %s,%s FROM Stock.stockPrediction_oneyearstock where name = "%s"' %(attr, attr2, name)
    cursor.execute(sql)
    results = cursor.fetchall()
    x = []
    y = []
    t = []
    for index in range(len(results) - n):
		x.append([e[0] for e in results[index : index + n]] + [e[1] for e in results[index : index + n]])
		y.append(results[index + n][0])
    t = x[-1][1:]
    t.append(y[-1])
    return (x, y, t)


#getSamples('AAPL', 'close')

def SVM(name, attr):
	x = getSamples(name, attr)[0]
	y = getSamples(name, attr)[1]
	t = getSamples(name, attr)[2]
	t = [t]
	clf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
	clf.fit(x, y)
	result = clf.predict(x[50:100])
	ans = y[50:100]
	relaterror = 0
	for e in range(50):
		relaterror = relaterror + abs((ans[e] - result[e])) / ans[e]
	relaterror = relaterror / 50
	print relaterror
	final = clf.predict(t)
	print final


	return (final, relaterror)

SVM('YHOO', 'close')

def getSamplesL(name, attr, attr2 = 'volume', n = 20, long = 5):
    cursor = connection.cursor()
    sql = 'SELECT %s,%s FROM Stock.stockPrediction_oneyearstock where name = "%s"' %(attr, attr2, name)
    cursor.execute(sql)
    results = cursor.fetchall()
    x = []
    y = []
    t = []
    for index in range(len(results) - n - long + 1):
        x.append([e[0] for e in results[index : index + n]] + [e[1] for e in results[index : index + n]])
        y.append([e[0] for e in results[index + n : index + n + long]])
    t = [e[0] for e in results[-n:]] + [e[1] for e in results[-n:]]
    return (x, y, t)

#getSamplesL('AAPL', 'close')

def ANN(name, attr):
	x = getSamplesL(name, attr)[0]
	y = getSamplesL(name, attr)[1]
	t = getSamplesL(name, attr)[2]
	net = buildNetwork(40, 250, 5)
	ds = SupervisedDataSet(40, 5)
	for e in range(len(x)):
		ds.addSample(x[e], y[e])
	trainer = BackpropTrainer(net, ds)
	for i in range(150):
		trainer.train()
	error = 0
	count = 0
	for i in range(len(x))[::10]:
		count = count + 1
		tresult = net.activate(x[i])
		ans = y[i]
		for j in range(len(ans)):
			error = error + abs(tresult[j] - ans[j]) / ans[j]

	error = error / (count * 5) / 4
	print error
#	tresults = x[50:100]

	result = net.activate(t)
	print result
	return (result, error)

#ANN('YHOO', 'close')

def getSamplesB(name, attr, attr2 = 'volume', n = 200):
    cursor = connection.cursor()
    sql = 'SELECT %s,%s FROM Stock.stockPrediction_oneyearstock where name = "%s"' %(attr, attr2, name)
    cursor.execute(sql)
    results = cursor.fetchall()
    y = []
    for index in range(len(results))[len(results) - n:]:
        y.append(results[index][0])
#	x = range(n)
    return (y,)

#getSamplesB('AAPL', 'close')

def BCF(name, attr, l = 20):
#	x = getSamplesB(name, attr)[0]
#	y = getSamplesB(name, attr)[1]
	y = getSamplesB(name, attr)[0]
	yt = y[len(y) - l:]
	x = range(l)
	alpha= 0.005
	beta= 11.1
	M = 3
	(s, phi) = bs.train(np.array(x), np.array(yt), alpha, beta, M)
	t = np.array([len(x)])
	resultf = bs.test(t, s, phi, beta)
	error = 0
	for i in range(150)[50:80]:
		yt = y[i : i + l]
		x = range(l)
		(s, phi) = bs.train(np.array(x), np.array(yt), alpha, beta, M)
		t = np.array([len(x)])
		result = bs.test(t, s, phi, beta)
		ans = y[i + l]
		error = error + abs(result[0][0] - ans) / ans
	error = error / 30
	print error
	print resultf[0]
	return (resultf[0], error)
BCF('YHOO', 'close')

def getRows(s, n, attr):
    if s == 'SVM':
        cursor = connection.cursor()
        cursor.execute('select %s,%s,%s from stockPrediction_oneyearstock where name = "%s"' % ('name', attr, 'time', n))
        rowlist = []
        for row in cursor.fetchall():
            d = collections.OrderedDict()
            d["name"] = row[0]
            d["pirce"] = row[1]
            d["time"] = row[2]
            rowlist.append(d)
        result = SVM(n, attr)
        d = collections.OrderedDict()
        d["name"] = n
        d["price"] = result[0][0]
        interval = timedelta(1)
        d["time"] = rowlist[0]["time"] + interval
        print d
        r = [d]

        return (r + rowlist)

    if s == 'Bayesian':
        cursor = connection.cursor()
        cursor.execute('select %s,%s,%s from stockPrediction_oneyearstock where name = "%s"' % ('name', attr, 'time', n))

        rowlist = []
        for row in cursor.fetchall():
            d = collections.OrderedDict()
            d["name"] = row[0]
            d["pirce"] = row[1]
            d["time"] = row[2]
            rowlist.append(d)
        result = BCF(n, attr)
        d = collections.OrderedDict()
        d["name"] = n
        d["price"] = result[0][0]
        interval = timedelta(1)
        d["time"] = rowlist[0]["time"] + interval
        r = [d]
        return r + rowlist

    if s == 'ANN':
        cursor = connection.cursor()
        cursor.execute('select %s,%s,%s from stockPrediction_oneyearstock where name = "%s"' % ('name', attr, 'time', n))
        rowlist = []
        rowlist = []
        for row in cursor.fetchall():
            d = collections.OrderedDict()
            d["name"] = row[0]
            d["pirce"] = row[1]
            d["time"] = row[2]
            rowlist.append(d)
        result = ANN(n, attr)
        for i in range(len(result[0])):
            d = collections.OrderedDict()
            d["name"] = n
            d["price"] = result[0][i]
            interval = timedelta(1)
            d["time"] = rowlist[0]["time"] + interval
            r = [d]
            rowlist = r + rowlist
        return rowlist









