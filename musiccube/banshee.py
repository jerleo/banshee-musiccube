#
# banshee.py
#
# Copyright (C) 2015 Jeremiah J. Leonard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sqlite3
import urllib

import gi
gi.require_version('GConf', '2.0')
from gi.repository import GConf

class Banshee:

    DB_PATH = ".config/banshee-1/banshee.db"
    GCONF_KEY = "/apps/banshee-1/sources/_music_library_source_-_library/library-location"

    class Connection:

        def __init__(self, db_path):

            self.db_path = db_path

        def __enter__(self):

            self.connection = sqlite3.connect(self.db_path)  # PyDev: Forced built-in _sqlite3
            return self.connection.cursor()

        def __exit__(self, type, value, traceback):  # @ReservedAssignment

            self.connection.close()
            return True

    def __init__(self):

        home = os.path.expanduser('~')
        self.db_path = os.path.join(home, self.DB_PATH)

    def library_source(self):

#        client = gconf.client_get_default()
        client = GConf.Client.get_default()
        source = client.get_string(self.GCONF_KEY)
        assert source, "GConf: %s not found" % self.GCONF_KEY
        return source

    def get_tracks(self):

        result = {}

        with self.Connection(self.db_path) as db:

            db.execute("""SELECT Uri, TrackId 
                            FROM CoreTracks
                           WHERE Uri LIKE 'file://%.mp3' 
                           ORDER BY Uri""")
            rows = db.fetchall()

        for row in rows:
            song = row[0].encode('ascii')
            song = urllib.unquote(song)
            song = song.replace("file://", "")
            if os.path.exists(song):
                result[song] = row[1]

        return result

    def create_table(self):

        with self.Connection(self.db_path) as db:

            db.executescript("""
                DROP TABLE IF EXISTS MusicCube;
                CREATE TABLE MusicCube ( 
                    TrackID INTEGER PRIMARY KEY,
                    Axis1   INTEGER,
                    Axis2   INTEGER,
                    Axis3   INTEGER );
                """)

    def update_tracks(self, song_positions):

        self.create_table()

        with self.Connection(self.db_path) as db:

            banshee_songs = self.get_tracks()

            for song in banshee_songs:
                if song in song_positions:
                    track_id = banshee_songs[song]
                    grid = song_positions[song]
                    db.execute("INSERT INTO MusicCube VALUES( ?, ?, ?, ? )",
                               (track_id, grid[0], grid[1], grid[2]))
            db.connection.commit()

