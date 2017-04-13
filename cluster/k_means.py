#!/usr/bin/python
#
#    Copyright 2017 Music Mojo
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""K-Means clustering algorithm for music data"""

import sys

import MySQLdb

import numpy
#import plot
import scipy.cluster


TRACK_TBL = "music_track_tbl"

HOST = "localhost"
USER = "root"
PSWD = "musicmojo"
DB = "song_recommender"

K = 2


def get_data():
    connection = MySQLdb.connect(host=HOST,
                                 user=USER,
                                 passwd=PSWD,
                                 db=DB)

    cursor = connection.cursor()

    try:
        query = "SELECT tempo,music_track_tbl.key,loudness,mode,segments_loudness_max,music_track_tbl.`time signature` from {} ORDER BY incrementing_id ASC".format(TRACK_TBL)
        cursor.execute(query)

        iterator = cursor.fetchall()
        dt = numpy.dtype([('tempo', numpy.float32),
                          ('music_track_tbl.key', numpy.int16),
                          ('loudness', numpy.float32),
                          ('mode', numpy.int16),
                          ('segments_loudness_max', numpy.float32),
                          ('music_track_tbl.`time signature`', numpy.int16)])
        data = numpy.fromiter(iterator, dt).astype(numpy.float)
        connection.close()
        return data
    except MySQLdb.Error as err:
        print "Failed to fetch data from DB: {}".format(err)
        connection.close()
        sys.exit(1)


def write_out_clusters(idx):
    tmp_mood_list = idx.tolist()
    mood_list = map(str, tmp_mood_list)
    connection = MySQLdb.connect(host=HOST,
                                 user=USER,
                                 passwd=PSWD,
                                 db=DB)

    cursor = connection.cursor()

    try:
        get_query = "SELECT incrementing_id from {} ORDER BY incrementing_id ASC".format(TRACK_TBL)
        cursor.execute(get_query)
        for incr_id, mood in zip(cursor, mood_list):
            write_cursor = connection.cursor()
            query = "INSERT INTO {} (mood) VALUES ({}) WHERE incrementing_id == {}".format(TRACK_TBL, mood, incr_id)
            write_cursor.execute(query)
            connection.commit()
        connection.close()
    except MySQLdb.Error as err:
        print "Failed to write out mood to DB: {}".format(err)
        connection.close()
        sys.exit(1)


def cluster():
    # Compute k-means with K centroids
    data = get_data()
    centroids,_ = scipy.cluster.vq.kmeans2(data, K)

    # assign each data point to a cluster
    idx,_ = scipy.cluster.vq.vq(data, centroids)

    return idx


if __name__ == "__main__":
    cluster()
