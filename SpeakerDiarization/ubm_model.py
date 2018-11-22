'''
Created on 24-Oct-2018

@author: anu
'''
from SpeakerDiarization.Features import mfcc
from sklearn.mixture import GaussianMixture 
from sklearn.externals import joblib
import os

path = os.getcwd() + '/SpeakerDiarization/SpeakerDiarization'

#Universal Background Model#global model
def UBMmodel(ubmfoldername, name, companyname, file):
    if file == '':
        features = mfcc(ubmfoldername, '')
        gmm = GaussianMixture(n_components = 8, max_iter = 200, 
                              covariance_type='diag', n_init = 3)
        gmm.fit(features)
        joblib.dump(gmm,  path + '/' + companyname + '_ubm_models/' + name + 'ubm.pkl')
