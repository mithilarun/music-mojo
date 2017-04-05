import sys
import os
import glob
import pymysql
import numpy as np
from song_tbl import *

song_tbl.init()
#data = song_tbl.getRowBySongId('SOAAAQN12AB01856D3')
#print('artist name : ', data[0][2])
#data = song_tbl.getRowById('18')
#print("title :", data[0][3])
#data = song_tbl.getRowsByIdRange('1','5')
#print("row data :", data[0])

#print("Mood:")
#for x in data:
#    song = song_tbl.getSong(x)
#    print(song.mood)

#data = song_tbl.runquery("select count(*) from music_track_tbl")
#print('Count: ', data[0][0])

#data = song_tbl.gettraindata('100','120')
#print(data)

data =song_tbl.gettrainlabels('100', '120')
print(data)
