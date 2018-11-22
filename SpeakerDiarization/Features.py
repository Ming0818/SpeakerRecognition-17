# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:01:13 2018

@author: Anu
"""

import librosa
import numpy as np
from .preprocess import denoise

def mfcc(name, file):
    if file == '':
        y, sr = denoise(name, '')
        features_list = []
        for i in y:
            mfcc = librosa.feature.mfcc(y=i, sr=sr, S=None, n_mfcc=13)#y = None,S= i for 2D 
            mfcc_delta = librosa.feature.delta(mfcc, order=1, mode='nearest')
            mfcc_delta2 = librosa.feature.delta(mfcc, order=2, mode='nearest')
            features_list.append(np.r_[mfcc, mfcc_delta, mfcc_delta2])
        feature_array = np.hstack(features_list)
        feature_array = np.transpose(feature_array)
        return feature_array
    else:
        y, sr = denoise(name, file)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, S=None, n_mfcc=13)
        mfcc_delta = librosa.feature.delta(mfcc, order=1, mode='nearest')
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2, mode='nearest')
        feature_array = np.r_[mfcc, mfcc_delta, mfcc_delta2]
        feature_array = np.transpose(feature_array)
        return feature_array
