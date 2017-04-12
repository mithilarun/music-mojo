import sys
import os
import glob
import pymysql
import numpy as np
from song_tbl import *

wordMap = {}
with open("AFINN-111.txt") as file:
    for line in file:
        (key, val) = line.split('\t')
        wordMap[str(key)] = int(val)

song_tbl.init()
lyricData = song_tbl.runquery("select * from song_lyrics order by incrementing_id asc")
for row in lyricData:
    inc_id = row[0]
    lyric = row[1]

    posSum = 0
    negSum = 0
    words = lyric.split()
    for word in words:
        if word in wordMap:
            if wordMap[word] > 0:
                posSum = posSum + wordMap[word]
            else:
                negSum = negSum = wordMap[word]

    
    total = posSum + negSum
    #print(total)
    song_tbl.insert("update music_track_tbl set `word frequency` = {} where incrementing_id = '{}'".format(total, inc_id))
