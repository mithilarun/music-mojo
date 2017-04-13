import sys
import os
import glob
import pymysql
import numpy as np
from sklearn import svm
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
print("Randlist size :" + str(len(randList)))

traindata = song_tbl.getDataFromList(randList)
trainlabels = song_tbl.getLabelsFromList(randList)
print("Train data size :" + str(len(traindata)))
print("Train label size :" + str(len(trainlabels)))
clf = svm.SVC()
clf.fit(traindata, trainlabels)

testdata = song_tbl.getDataNotInList(randList)
testlabels = song_tbl.getLabelsNotInList(randList)
print("Test data size:" + str(len(testdata)))
print("Test label size :" + str(len(testlabels)))

pred = clf.predict(testdata)
print('SVM accuracy : ' + str("{0:.2f}".format(float(accuracy_score(testlabels, pred))*100)) + "%")
