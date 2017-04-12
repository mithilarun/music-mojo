import sys
import os
import glob
import pymysql
import numpy as np
import subprocess
import re

from subprocess import *
from song_tbl import *

song_tbl.init()
data = song_tbl.runquery("SELECT * FROM music_track_tbl order by incrementing_id asc");
count = 0;
for row in data:
    song = song_tbl.getSong(row);
    inc_id = song.inc_id
    
    proc = subprocess.Popen(['lyrics', song.artist_name, song.title], stdout=subprocess.PIPE)
    lyrics = proc.stdout.read()
    #print(lyrics)

    if b'ERROR: ' not in lyrics:
        lyrics = re.sub("[^a-zA-Z]", " ", str(lyrics))
        str1 = "INSERT INTO song_lyrics (incrementing_id, lyrics) VALUES ( {}, {})".format(str(inc_id), str(lyrics[:511]))
#        print("query :" + str1)
        song_tbl.insert("INSERT INTO song_lyrics (incrementing_id, lyrics) VALUES ( {}, '{}')".format(str(inc_id), str(lyrics[:511])))
