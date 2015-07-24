# Original code by:
#   Alex Wiltschko: A Kohonen Map in Python (optimized by Numba)
#   http://nbviewer.ipython.org/gist/alexbw/3407544

import numpy as np
import os

from numba import jit
from progress import Progress

class NumbaCube:

    def __init__(self, edge_length, node_weights, npy_path=None, random_seed=None):

        # Seed random generator
        np.random.seed(random_seed)

        self.edge_length = edge_length
        self.nodes = edge_length ** 3
        self.dims = node_weights

        raw_grid = np.mgrid[0:edge_length, 0:edge_length, 0:edge_length]

        self.indices = np.zeros((self.nodes, 3))
        self.indices[:, 0] = raw_grid[0].ravel()
        self.indices[:, 1] = raw_grid[1].ravel()
        self.indices[:, 2] = raw_grid[2].ravel()

        if not npy_path == None:
            base_name = os.path.join(npy_path, "numbacube_%sx%sx%s" % 
                                     (edge_length, edge_length, edge_length))
            self.weight_file = base_name + '.npy'

        # Initialize the weights
        if os.path.exists(self.weight_file):
            self.weights = np.load(self.weight_file)
            self.new = False
        else:
            self.weights = np.random.random((self.nodes, self.dims))
            self.new = True

        # Allocate the weight distances
        self.distances = np.zeros((self.nodes,), dtype='d')

    def get_position(self, sample):

        winner = get_winner(sample, self.nodes, self.dims,
                            self.weights, self.distances)
        x = int(self.indices[winner, 0])
        y = int(self.indices[winner, 1])
        z = int(self.indices[winner, 2])
        return (x, y, z)

    def save(self):

        if not self.weight_file == None:
            np.save(self.weight_file, self.weights)
            return True
        return False

    def scale(self, start, end):

        return np.double(start + self.progress * (end - start))

    def train(self, data):

        # Some initial logistics
        samples, dims = data.shape

        # Check shape
        assert(dims == self.dims)

        # Set parameters
        rate_lower = 0.1
        rate_upper = 0.5

        spread_lower = 0.01

        if self.new:
            # Large spread for fresh weights
            spread_upper = self.edge_length / 3.0
        else:
            # Small spread for trained weights
            spread_upper = spread_lower * 1.5

        shuffled = range(samples)
        np.random.shuffle(shuffled)

        # Create progress object
        progress = Progress("Training MusicCube", samples)

        for ix in range(samples):

            # Pick a random vector
            sample = data[shuffled[ix], :]

            # Figure out who's the closest weight vector
            # and calculate distances between weights and the sample
            winner = get_winner(sample, self.nodes, self.dims,
                                self.weights, self.distances)

            # Calculate the new learning rate and new learning spread
            self.progress = float(ix) / float(samples)
            self.rate = self.scale(rate_upper, rate_lower)
            self.spread = self.scale(spread_upper, spread_lower)

            # Update those weights
            update_weights(sample, winner,
                           self.nodes, self.dims,
                           self.rate, self.spread,
                           self.weights, self.indices)

            # Display progress
            progress.display()

@jit(nopython=True)
def get_winner(sample, nodes, dims, weights, distances):

    for n in range(nodes):
        distances[n] = 0.0
        for d in range(dims):
            distances[n] += (sample[d] - weights[n, d]) ** 2.0
        distances[n] **= 0.5
    return np.argmin(distances)

@jit(nopython=True)
def update_weights(sample, winner, nodes, dims, rate, spread, weights, indices):

    x = indices[winner, 0]
    y = indices[winner, 1]
    z = indices[winner, 2]

    for n in range(nodes):
        distance = ((x - indices[n, 0]) ** 2.0) + \
                   ((y - indices[n, 1]) ** 2.0) + \
                   ((z - indices[n, 2]) ** 2.0)
        distance **= 0.5
        dampening = np.e ** (-distance / (2.0 * spread ** 2.0))
        dampening *= rate

        for d in range(dims):
            weights[n, d] += dampening * (sample[d] - weights[n, d])
