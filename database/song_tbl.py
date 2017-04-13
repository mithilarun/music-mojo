import sys
import os
import glob
import pymysql
import numpy as np

class song_tbl():

    def __init__(self, x):
        self.inc_id = x[0]
        self.song_id = x[1]
        self.title = x[2]
        self.artist_familiarity = x[3]
        self.artist_hotness = x[4]
        self.song_hotness = x[5]
        self.tempo = x[6]
        self.key = x[7]
        self.loudness = x[8]
        self.mode = x[9]
        self.segments_loudness_max = x[10]
        self.time_signature = x[11]
        self.word_frequency = x[12]
        self.mood = x[13]

    #initialize a connection to song_recommender database
    @classmethod
    def init(cls):
        global conn
        conn = pymysql.connect(host= 'localhost', user='root', passwd='password', db='song_recommender')

    #get a single row from song table using song_id
    @classmethod
    def getRowBySongId(cls, song_id):
        cursor = conn.cursor()
        query = "SELECT * FROM music_track_tbl WHERE song_id = %s"
        cursor.execute(query, song_id)
        data = cursor.fetchall()
        return data

    #get a single row from song table using incrementing id
    @classmethod
    def getRowById(cls, inc_id):
        cursor = conn.cursor()
        query = "SELECT * FROM music_track_tbl WHERE incrementing_id = %s"
        cursor.execute(query, inc_id)
        data = cursor.fetchall()
        return data

    #get multiple rows from song table using range of incrementing id
    @classmethod
    def getRowsByIdRange(cls, id_start, id_end):
        cursor = conn.cursor()
        query = "SELECT * FROM music_track_tbl WHERE incrementing_id BETWEEN %s AND %s"
        cursor.execute(query, (id_start, id_end))
        data = cursor.fetchall()
        return data

    #get a song_tbl object by from a row
    @classmethod
    def getSong(cls, x):
        return cls(x)

    #run a query on the table
    @classmethod
    def runquery(cls, query):
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
