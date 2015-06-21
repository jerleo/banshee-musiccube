# Original code by:
#   Christian Peccei: Mapping Your Music Collection
#   http://www.christianpeccei.com/musiccube/

import numpy as np
import os
import struct
import wave

from shlex import split
from subprocess import call
from uuid import uuid4

class Analyzer:

    FEATURES_LENGTH = 42
    SECONDS_PER_SONG = 90
    SAMPLING_RATE = 10000

    def valid_features(self, data):

        return len(data) == self.FEATURES_LENGTH

    def moments(self, x):

        mean = x.mean()
        std = x.var() ** 0.5
        skewness = ((x - mean) ** 3).mean() / std ** 3
        kurtosis = ((x - mean) ** 4).mean() / std ** 4

        return [mean, std, skewness, kurtosis]

    def fftfeatures(self, wavdata):

        f = np.fft.fft(wavdata)
        f = f[2:(f.size / 2 + 1)]
        f = abs(f)
        total_power = f.sum()
        f = np.array_split(f, 10)

        return [e.sum() / total_power for e in f]

    def features(self, data):

        # convert to array
        x = np.array(data)

        # initialize result vector
        feature_vec = np.zeros(self.FEATURES_LENGTH)

        # smoothing window: 1 samples
        x1 = x
        d1 = x1[1:] - x1[:-1]
        feature_vec[0:4] = self.moments(x1)
        feature_vec[4:8] = self.moments(d1)

        # smoothing window: 10 samples
        x10 = x.reshape(-1, 10).mean(1)
        d10 = x10[1:] - x10[:-1]
        feature_vec[8:12] = self.moments(x10)
        feature_vec[12:16] = self.moments(d10)

        # smoothing window: 100 samples
        x100 = x.reshape(-1, 100).mean(1)
        d100 = x100[1:] - x100[:-1]
        feature_vec[16:20] = self.moments(x100)
        feature_vec[20:24] = self.moments(d100)

        # smoothing window: 1000 samples
        x1000 = x.reshape(-1, 1000).mean(1)
        d1000 = x1000[1:] - x1000[:-1]
        feature_vec[24:28] = self.moments(x1000)
        feature_vec[28:32] = self.moments(d1000)

        feature_vec[32:] = self.fftfeatures(data)

        return feature_vec

    def read_wav(self, wav_file):

        song_data = wave.open(wav_file)
        n = song_data.getnframes()
        n = n - n % 1000
        frames = song_data.readframes(n)
        wav_data = struct.unpack('%dh' % n, frames)

        return wav_data

    def compute_features(self, mp3_file):

        out_path = '/tmp/%s.wav' % uuid4()
        cmd_args = 'avconv -v quiet -i "%s" -ac 1 -ar %s -t %s "%s"'
        cmd_args = cmd_args % (mp3_file, self.SAMPLING_RATE,
                               self.SECONDS_PER_SONG, out_path)

        ret_code = call(split(cmd_args))
        assert(ret_code == 0)

        sample_data = self.read_wav(out_path)
        assert(len(sample_data) > 0)

        os.remove(out_path)

        return self.features(sample_data)

