'''
Created on 16-Nov-2018

@author: anu
'''
from SpeakerDiarization.Features import mfcc
from sklearn.externals import joblib
from .views import db
from .Recognition import recognition
import os
import warnings
warnings.filterwarnings("ignore")

path = os.getcwd() + '/SpeakerDiarization/SpeakerDiarization'

def predict(companyname):
    gmm_models = os.listdir(path + '/' + companyname + '_speaker_models')# total files
    print(gmm_models)
    sliced_files = os.listdir(path + '/' + companyname + '_sliced')
    ubm_files =os.listdir(path + '/' + companyname + '_ubm_models')
    print(sliced_files)
    final_list = []
    for i in sliced_files:
        print(i)
        for index,j in enumerate(gmm_models):
            print(j)
            login_features = mfcc(companyname, path + '/' + companyname + '_sliced/' + i)
            gmm = joblib.load(path + '/' + companyname + '_speaker_models/' + j)
            ubm = joblib.load(path + '/' + companyname + '_ubm_models/' + ubm_files[index])
            recognize = recognition(path + '/' + companyname + '_sliced/' + i)
            gmm_likelihood_score = gmm.score(login_features)#features of incoming voice
            print(gmm_likelihood_score)
            ubm_likelihood_score = ubm.score(login_features)#features of incoming voice 
            print(ubm_likelihood_score)
            likelihood_score = gmm_likelihood_score - ubm_likelihood_score
            print(likelihood_score)
            result = {}
            if likelihood_score > 0:
                result['user'] =j.split('.')[0]
                result['content'] = recognize
                final_list.append(result)
#             elif likelihood_score < 0:
#                 if index == (len(sliced_files)-1) :
#                     result['user'] ='Unsigned user'
#                     result['content'] = recognize
#                     final_list.append(result)
            
    print(final_list)
    print(len(final_list))
    return final_list

    
                