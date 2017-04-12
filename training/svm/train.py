import sys
import os
import glob
import pymysql
import numpy as np
from sklearn import svm
from song_tbl import *
from sklearn.metrics import accuracy_score
import random

song_tbl.init()
count = song_tbl.runquery("select count(*) from music_track_tbl")
#count_list = range(1,count[0][0])
incIds = song_tbl.runquery("select incrementing_id from music_track_tbl order by incrementing_id asc")
incIdList = []
for incId in incIds:
	incIdList.append(incId[0])

#print(incIdList)
randList = random.sample(incIdList, int((3/float(4))*count[0][0]))
print("Randlist size :" + str(len(randList)))
#print("Training size is " + str(len(randList)))

#traindata = song_tbl.runquery("select * from music_track_tbl where incrementing_id in {} order by incrementing_id asc".format(tuple(rand)))
traindata = song_tbl.getDataFromList(randList)
trainlabels = song_tbl.getLabelsFromList(randList)
print("Train data size :" + str(len(traindata)))
print("Train label size :" + str(len(trainlabels)))
#print(X)
#print(y)
#y = np.reshape(y,(1,1000))
clf = svm.SVC()
clf.fit(traindata, trainlabels)

testdata = song_tbl.getDataNotInList(randList)
testlabels = song_tbl.getLabelsNotInList(randList)
print("Test data size:" + str(len(testdata)))
print("Test label size :" + str(len(testlabels)))

pred = clf.predict(testdata)
#print(pred) 
print(accuracy_score(testlabels, pred))
