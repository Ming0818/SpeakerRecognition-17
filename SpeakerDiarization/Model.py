# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:34:20 2018

@author: Anu
"""

from SpeakerDiarization.Features import mfcc
from sklearn.mixture import GaussianMixture 
from sklearn.externals import joblib
import os

path = os.getcwd() + '/SpeakerDiarization/SpeakerDiarization'

def model(name,companyname, file):#one time model building 
    if file == '':
        features = mfcc(name, '')
        gmm = GaussianMixture(n_components = 8, max_iter = 200, 
                              covariance_type='diag', n_init = 3)
        gmm.fit(features)
        #dump 5 training samples #for likelihood score
        joblib.dump(gmm, path + '/' + companyname + '_speaker_models/' + name + '.pkl') 
        #dump mfcc features of 5 training samples# required for cosine similarity
#         joblib.dump(features, path + '/speaker_models/' + login + 'features.pkl')
    response = {}
    response['message'] = 'Model successfully built'
    return response
