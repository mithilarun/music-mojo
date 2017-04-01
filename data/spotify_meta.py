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
"""Fetch Song Meta Data from Spotify"""

import json
import sys
import urllib

import base64
#import pymysql
import MySQLdb
import requests


CLIENT_ID = "bed1f40ecba8403fb22ddecc36bf628a"
CLIENT_SECRET = "e4ef6918fa484813ac9108a16ab009fc"
TRACK_TBL = "music_track_tbl"
SPOTIFY_META_TBL = "spotify_meta"

HOST = "localhost"
USER = "root"
PSWD = "musicmojo"
DB = "song_recommender"

COUNT = 1


def get_song_name():
    """Return the song name and artist"""
    global COUNT
    connection = MySQLdb.connect(host=HOST,
                                 user=USER,
                                 passwd=PSWD,
                                 db=DB)

    cursor = connection.cursor()
    try:
        query = "SELECT title,song_id,artist_name FROM {} ".format(
                TRACK_TBL) +\
                "LIMIT 2 OFFSET {}".format(
                COUNT)
        cursor.execute(query)

        COUNT += 1

        for artist, songid, track in cursor:
            if track == 'title':
                continue
            print songid, track, artist
            return songid, track, artist
    except MySQLdb.Error as err:
        print "Something went wrong: {}. Exiting.".format(err)
        sys.exit(1)


def get_api_token():
    """Generate an API token at Spotify"""
    endpoint = "https://accounts.spotify.com/api/token"
    params = {"grant_type": "client_credentials"}
    secret = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    header = {"Authorization": "Basic {}".format(secret)}

    response = requests.post(endpoint, headers=header, data=params)
    if response.status_code != 200:
        print response.content
        print "Failed to get an API token. Exiting."
        sys.exit(1)

    response_list = json.loads(response.content)
    return response_list["access_token"]


def get_song_id(song, artist):
    """Fetch Spotify ID of song using its name and artist"""
    if song == "":
        print "Song name empty. Cannot proceed"
        return False

    artist = urllib.quote(artist)
    song = urllib.quote(song)
    endpoint = 'https://api.spotify.com/v1/search?' +\
               'q=artist:"{}"%20track:"{}"&type=track'.format(artist, song)
    print endpoint
    response = requests.get(endpoint)
    if response.status_code != 200:
        print "Failed to get song name with error %s" %(response.status_code)
        return False

    response_list = json.loads(response.content)
    if  len(response_list["tracks"]["items"]) == 0:
        print "Not enough results from server"
        return False

    return response_list["tracks"]["items"][0]["id"]


def get_song_meta(song_id, api_token):
    """Fetch Spotify metadata of a song using its ID"""
    if api_token == "":
        print "Failed to fetch song metadata. API token missing"
        sys.exit(1)

    endpoint = "https://api.spotify.com/v1/audio-features/{}".format(song_id)
    headers = {"Authorization": "Bearer %s" %(api_token)}
    print endpoint
    print headers
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print "Failed to get song attributes. Error code - %s" \
              %(response.status_code)
        return False

    response_list = json.loads(response.content)
    return response_list


def create_meta_table():
    connection = MySQLdb.connect(host=HOST,
                                 user=USER,
                                 passwd=PSWD,
                                 db=DB)

    cursor = connection.cursor()

    query = "CREATE TABLE {} (".format(SPOTIFY_META_TBL) +\
            "meta_id int NOT NULL AUTO_INCREMENT, " +\
            "song_id varchar(20), " +\
            "danceability decimal(3,3), " +\
            "energy decimal(3,3), " +\
            "key int, " +\
            "loudness decimal(3,3), " +\
            "mode boolean, " +\
            "speechiness decimal(3,3), " +\
            "acousticness decimal(3,3), " +\
            "instrumentalness decimal(3,3), " +\
            "liveness decimal(3,3), " +\
            "valence decimal(3,3), " +\
            "tempo decimal(3,3), " +\
            "type varchar(20), " +\
            "id varchar(30), " +\
            "uri varchar(50), " +\
            "track_href varchar(100), " +\
            "analysis_url varchar(100), " +\
            "duration_ms int, " +\
            "time_signature int, " +\
            "PRIMARY KEY (meta_id), " +\
            "FOREIGN KEY (song_id) REFERENCES {}(song_id))".format(TRACK_TBL)

    try:
        cursor.execute(query)
        connection.commit()
    except MySQLdb.Error as err:
        print "Something bad happened while creating the meta table: {}".format(err)
        sys.exit(1)


def save_meta(tbl_id, meta_data):
    """Save generated Spotify metadata"""
    print meta_data
    return ""


def main():
    """Script controller"""
    #
    # ALGORITHM:
    # 1. Read song name from file
    # 2. Fetch ID of song from Spotify
    # 3. Using ID, fetch song metadata from Spotify
    # 4. Dump metadata JSON to output file
    #
    create_meta_table()
    api_token = get_api_token()

    while True:
        meta_data = False
        tbl_id, song, artist = get_song_name()
        song_id = get_song_id(song, artist)
        if song_id is not False:
		meta_data = get_song_meta(song_id, api_token)
        if meta_data is not False:
		save_meta(tbl_id, meta_data)


if __name__ == "__main__":
    main()
