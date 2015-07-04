#
# musiccube.py
#
# Copyright (C) 2015 Jeremiah Leonard
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

import numpy as np
import os
import shelve

from analyzer import Analyzer
from banshee import Banshee
from numbacube import NumbaCube

class MusicCube:

    # number of neurons per edge of cube
    SOM_SIZE = 42

    # path and file name of music database
    DB_PATH = ".musiccube"
    DB_NAME = "musiccube.dbm"

    # normalize data
    SCALE = True

    def __init__(self):

        # get music path from Banshee
        self.banshee = Banshee()
        self.music_path = self.banshee.library_source()

        # get full path of music database
        db_path = os.path.join(self.music_path, self.DB_PATH)
        db_file = os.path.join(db_path, self.DB_NAME)

        # create path to music database
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        # get and update music data
        self.music_shelve = shelve.open(db_file, writeback=True)
        self.update_music_data()

        if self.SCALE:
            self.scale_music_data()
        
        # create or load music cube        
        self.numba_cube = NumbaCube(
            edge_length=self.SOM_SIZE,
            node_weights=Analyzer.FEATURES_LENGTH,
            npy_path=db_path,
            random_seed=1)

    def __del__(self):

        self.music_shelve.close()

    def get_paths(self):

        return self.music_shelve.keys()

    def get_features(self, song):

        # calculate scaled song features
        song_data = np.array(self.music_shelve[song])

        # normalize by column
        if self.SCALE:
            song_data = self.scale_by_column(song_data)

        return song_data

    def get_position(self, song):

        # return cube coordinates of song
        song_features = self.get_features(song)
        return self.numba_cube.get_position(song_features)

    def update_music_data(self):

        analyzer = Analyzer()
        music_list = self.banshee.get_tracks()
        song_count = len(music_list)
        processed = 0
        
        # delete previously analyzed songs no longer existing in Banshee
        for mp3 in self.music_shelve:
            if mp3 not in music_list:
                del self.music_shelve[mp3]
                self.music_shelve.sync()
                print "Dropped " + mp3

        # calculate and save features of new songs
        for mp3 in music_list:
            if mp3 not in self.music_shelve:
                features = analyzer.compute_features(mp3)
                if analyzer.valid_features(features):
                    self.music_shelve[mp3] = features
                    self.music_shelve.sync()
                    print "Analyzed " + mp3
                    
            processed += 1
            if processed % 50 == 0:
                progress = float(processed) / float(song_count)
                print "{:8.2f} %".format(progress * 100)

        # convert music data to array
        self.music_data = np.array(self.music_shelve.values())

    def update_banshee(self):

        # update song positions in Banshee
        positions = {}
        paths = self.get_paths()
        for song in paths:
            positions[song] = self.get_position(song)
        self.banshee.update_tracks(positions)

    def scale_music_data(self):

        # scale music data column wise
        mins = np.min(self.music_data, axis=0)
        self.maxs = np.max(self.music_data, axis=0)
        self.rng = self.maxs - mins
        self.music_data = self.scale_by_column(self.music_data)

    def scale_by_column(self, data, high=1.0, low=0.0):

        return high - (((high - low) * (self.maxs - data)) / self.rng)

    def train_numbacube(self):

        self.numba_cube.train(self.music_data)
        self.numba_cube.save()

if __name__ == '__main__':

    print "Analyzing Songs ..."
    music_cube = MusicCube()
    
    print "Training MusicCube ..."
    music_cube.train_numbacube()

    print "Updating Banshee ..."
    music_cube.update_banshee()

