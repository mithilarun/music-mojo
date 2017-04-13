import sys
import os
import glob
import pymysql
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn import neighbors,datasets
from sklearn.metrics import accuracy_score
import random
sys.path.append('../../database')
from song_tbl import *

song_tbl.init()
count = song_tbl.runquery("select count(*) from music_track_tbl")
incIds = song_tbl.runquery("select incrementing_id from music_track_tbl order by incrementing_id asc")
incIdList = []
for incId in incIds:
	incIdList.append(incId[0])

randList = random.sample(incIdList, int((3/float(4))*count[0][0]))

traindata = song_tbl.getDataFromList(randList)
trainlabels = song_tbl.getLabelsFromList(randList)
print("Train data size :" + str(len(traindata)))
print("Train label size :" + str(len(trainlabels)))

testdata = song_tbl.getDataNotInList(randList)
testlabels = song_tbl.getLabelsNotInList(randList)
print("Test data size:" + str(len(testdata)))
print("Test label size :" + str(len(testlabels)))
print()

clf = svm.SVC()
clf.fit(traindata, trainlabels)
pred = clf.predict(testdata)
print('SVM accuracy : '  + str("{0:.2f}".format(float(accuracy_score(testlabels, pred))*100)) + "%")

clf = RandomForestClassifier(n_estimators=10)
clf.fit(traindata, trainlabels)
pred = clf.predict(testdata)
print('Random Forest accuracy : ' + str("{0:.2f}".format(float(accuracy_score(testlabels, pred))*100)) + "%")

clf = linear_model.LogisticRegression(C=1e5)
clf.fit(traindata, trainlabels)
pred = clf.predict(testdata)
print('Logistic Regression accuracy : ' + str("{0:.2f}".format(float(accuracy_score(testlabels, pred))*100)) + "%")

clf = neighbors.KNeighborsClassifier(200, weights='uniform')
clf.fit(traindata, trainlabels)
pred = clf.predict(testdata)
print('KNN accuracy : ' + str("{0:.2f}".format(float(accuracy_score(testlabels, pred))*100)) + "%")

print()
