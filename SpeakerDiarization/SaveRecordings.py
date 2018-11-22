# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:06:13 2018

@author: Anu
"""

import os
import uuid
from pydub import AudioSegment
import io
from pydub.utils import which

path = os.getcwd() + '/SpeakerDiarization/SpeakerDiarization'

#Company registration 
def Register(companyname):
    response ={}
    if companyname != '':
        folder_list = os.listdir(path)
        if companyname+'_speaker_models' not in folder_list:
            companypath = path+'/'
            os.mkdir(companypath+companyname+'_speaker_models')
            os.mkdir(companypath+companyname+'_ubm_models')
            response['message'] ='Company registered'
            return response
        else:
            response['message'] = 'Company already registered'
            return response
    else:
        response['message'] = 'Please enter the company name'
        return response

        
# signing up using voice # company specific
def folder(name,companyname):
    response = {}
    if name!= '' and companyname != '':
        current_path = path + '/' +companyname+'_speaker_models'
        file_list = os.listdir(current_path)
        if name + '.pkl' in file_list:
            response['message'] = 'User already exists.'
            return response   
        else:
            try:
                os.mkdir(path + '/' + name)
                response['message'] = 'Sign Up successful.'
                return response
            except:
                response['message'] = 'User already exists.'
                return response
                
    else:
        response['message'] = 'Please enter the input'
        return response 
    
# Volume adjustment function      
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


#saving 5 training samples to the folder with user name
def save(name, file):
    if name != '':
        try:
            current_path = path + '/' + name
            for chunk in file.chunks():
                AudioSegment.converter = which("ffmpeg")
                Audio = AudioSegment.from_file(io.BytesIO(chunk), format="mp3")
                normalized_audio = match_target_amplitude(Audio, -20.0)
                file_path = os.path.join(current_path, name + uuid.uuid4().hex) 
                ubmfile_path = os.path.join(path + '/' + 'UBM', name + uuid.uuid4().hex)
                normalized_audio.export(file_path + '.wav', format="wav")
                normalized_audio.export(ubmfile_path + '.wav', format='wav')
        except:
            pass
