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
import plot
import scipy


TRACK_TBL = "music_track_tbl"

HOST = "localhost"
USER = "root"
PSWD = "musicmojo"
DB = "song_recommender"

K = 10


def get_data():
    connection = MySQLdb.connect(host=HOST,
                                 user=USER,
                                 passwd=PSWD,
                                 db=DB)

    cursor = connection.cursor()

    try:
        query = "SELECT * from {}".format(TRACK_TBL)
        cursor.execute(query)

        iterator = cursor.fetchall()
        data = numpy.fromiter(iterator, numpy.float)
        connection.close()
        return data
    except MySQLdb.Error as err:
        print "Failed to fetch data from DB: {}".format(err)
        connection.close()
        sys.exit(1)


def cluster():
    # Compute k-means with K centroids
    data = get_data()
    centroids,_ = scipy.cluster.vq.kmeans(data, K)

    # assign each data point to a cluster
    idx,_ = scipy.cluster.vq.vq(data, centroids)

    # plot the clusters to get a better idea of what it looks like
    pylab.plot(data[idx==0,0], data[idx==0,1], 'ob',
               data[idx==1,0], data[idx==1,1], 'or')
    pylab.plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
    pylab.show()


if __name__ == "__main__":
    cluster()
