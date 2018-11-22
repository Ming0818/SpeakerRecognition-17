'''
Created on 16-Nov-2018

@author: anu
'''
import os
from .views import seg
import uuid
from .SaveRecordings import match_target_amplitude
from pydub import AudioSegment
path = os.getcwd()+ '/SpeakerDiarization/SpeakerDiarization'


def Segment(file_name):
    
    segmentation = seg(file_name)
    print (segmentation)
    time_list = []
    for i in segmentation:
        if i[0] == 'Female' or i[0] == 'Male':
            time_list.append((i[1] , i[2]))
    return time_list
 
def AudioSlicing(file_name,companyname):
    output = Segment(file_name)
    audio = AudioSegment.from_wav(file_name)
    os.mkdir(path + '/' + companyname + '_sliced')
    currentpath = path + '/' + companyname + '_sliced'
    for i,j in output:
        segment = audio[i*1000:j*1000]
        normalized_audio = match_target_amplitude(segment, -20.0)
        normalized_audio.export(currentpath + '/' + uuid.uuid4().hex + '.wav',format = 'wav')

    
    