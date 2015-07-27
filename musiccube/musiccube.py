#
# musiccube.py
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

import numpy as np
import os
import shelve

from analyzer import Analyzer
from banshee import Banshee
from numbacube import NumbaCube
from progress import Progress

from matplotlib import pyplot, colors
from mpl_toolkits.mplot3d import Axes3D
from pylab import figure

class MusicCube:

    # path and file name of music database
    DB_PATH = ".musiccube"
    DB_NAME = "musiccube.dbm"

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

        # transform columns to be between 0 and 1
        self.scale_music_data()

        # calculate number of nodes per edge
        cube_edge = int(len(self.music_data) ** (1 / 3.0))

        # create or load music cube        
        self.numba_cube = NumbaCube(
            edge_length=cube_edge,
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
        song_data = self.scale_by_column(song_data)

        return song_data

    def get_position(self, song):

        # return cube coordinates of song
        song_features = self.get_features(song)
        return self.numba_cube.get_position(song_features)

    def update_music_data(self):

        analyzer = Analyzer()
        music_list = self.banshee.get_tracks()

        # delete previously analyzed songs no longer existing in Banshee
        for mp3 in self.music_shelve:
            if mp3 not in music_list:
                del self.music_shelve[mp3]
                self.music_shelve.sync()

        song_count = len(music_list)
        progress = Progress("Analyzing Songs", song_count)

        # calculate and save features of new songs
        for mp3 in music_list:
            if mp3 not in self.music_shelve:
                features = analyzer.compute_features(mp3)
                if analyzer.valid_features(features):
                    self.music_shelve[mp3] = features
                    self.music_shelve.sync()

            progress.display()

        # convert music data to array
        self.music_data = np.array(self.music_shelve.values())

    def update_banshee(self):

        self.counter = {}
        positions = {}
        paths = self.get_paths()
        song_count = len(paths)
        progress = Progress("Updating Banshee", song_count)

        for song in paths:
            position = self.get_position(song)
            positions[song] = position

            # count song positions for plotting
            if position not in self.counter:
                self.counter[position] = 1
            else:
                self.counter[position] += 1

            progress.display()

        # update song positions in Banshee
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

    def plot(self):

        # create and show scatter plot
        ax = Axes3D(figure())

        # transform to array
        data = np.array([(key[0], key[1], key[2], val)
                         for key, val in self.counter.items()])

        # sort by position counter
        data = data[np.argsort(data[:, 3])]

        # minimum and maximum counter
        min = np.min(data[:, 3])
        max = np.max(data[:, 3])

        # setup color mapping
        colormap = pyplot.cm.ScalarMappable(
            norm=colors.Normalize(vmin=min, vmax=max),
            cmap=pyplot.cm.get_cmap('RdYlBu_r'))

        # initialize group
        group = 0

        for ix in range(len(data)):

            # determine current group
            count = data[ix][3]

            # group header
            if not count == group:
                xs = []
                ys = []
                zs = []

            # group body
            xs.append(data[ix][0])
            ys.append(data[ix][1])
            zs.append(data[ix][2])
            group = count

            # group footer
            # last item or last item of group
            if (ix == len(data) - 1) or not (data[ix + 1][3] == group):
                color = colormap.to_rgba(group)
                size = group * 10
                ax.scatter(xs, ys, zs, c=color, s=size)

        ax.set_title("MusicCube")
        pyplot.show()

if __name__ == '__main__':

    music_cube = MusicCube()
    music_cube.train_numbacube()
    music_cube.update_banshee()
    music_cube.plot()
    print "Done."
