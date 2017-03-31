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
import pymysql
import requests


CLIENT_ID = "bed1f40ecba8403fb22ddecc36bf628a"
CLIENT_SECRET = "0f0f958fb06e4a5a92f4b2c70ea81f34"
TRACK_TBL = "music_track_tbl"

COUNT = 1


def get_song_name():
    """Return the song name and artist"""
    connection = pymysql.connect(host=HOST,
                                 user=USER,
                                 password=PSWD,
                                 db=DB,
                                 charset="utf8mb4",
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            query = "SELECT track,song_id,artist FROM {} LIMIT 1 OFFSET {}".format(
                    TRACK_TBL, COUNT)
            cursor.execute(query)

            COUNT += 1

            for songid, track, artist in cursor:
                return songid, track, artist
    except pymysql.Error:
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
        sys.exit(1)

    artist = urllib.quote(artist)
    song = urllib.quote(song)
    endpoint = 'https://api.spotify.com/v1/search?' +\
               'q=artist:"{}"%20track:"{}"&type=track'.format(artist, song)
    print endpoint
    response = requests.get(endpoint)
    if response.status_code != 200:
        print "Failed to get song name with error %s" %(response.status_code)
        sys.exit(1)

    response_list = json.loads(response.content)
    if  len(response_list["tracks"]["items"]) == 0:
        print "Not enough results from server"
        sys.exit(1)

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
        sys.exit(1)

    response_list = json.loads(response.content)
    return response_list


def save_meta(meta_data):
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
    api_token = get_api_token()

    while True:
        tbl_id, song, artist = get_song_name()
        song_id = get_song_id(song, artist)
        meta_data = get_song_meta(song_id, api_token)
        save_meta(tbl_id, meta_data)


if __name__ == "__main__":
    main()
