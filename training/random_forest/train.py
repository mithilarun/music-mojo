import sys
import os
import glob
import pymysql
import numpy as np
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, '../../database/')
from mysql_tbl_get import *

from sklearn.metrics import accuracy_score

train_start_val = 1
train_end_val = 14000
test_start_val = 14000
test_end_val = 16000
song_tbl.init()
traindata = song_tbl.gettraindata(train_start_val, train_end_val)
trainlabels = song_tbl.gettrainlabels(train_start_val,train_end_val)
#print(X)
#print(y)
#y = np.reshape(y,(1,1000))

clf = RandomForestClassifier(n_estimators=10)
clf.fit(traindata, trainlabels)

testdata = song_tbl.gettraindata(test_start_val, test_end_val)
testlabels = song_tbl.gettrainlabels(test_start_val, test_end_val)
pred = clf.predict(testdata)
print(pred) 
print(accuracy_score(testlabels, pred))