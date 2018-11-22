'''
Created on 08-Nov-2018

@author: anu
'''

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from .SaveRecordings import folder, save, match_target_amplitude,Register
from .Model import model
from .ubm_model import UBMmodel
from pydub import AudioSegment
from pymongo import MongoClient
from inaSpeechSegmenter import Segmenter
import io
import os 
import uuid
import shutil
import warnings
warnings.filterwarnings("ignore")

seg = Segmenter()

from SpeakerDiarization.Segmentation import AudioSlicing


path = os.getcwd() + '/SpeakerDiarization/SpeakerDiarization'
connection = MongoClient('52.221.4.121', 38128)
db = connection.convoRecording
from .prediction import predict

@permission_classes((permissions.AllowAny,))
class RegisterCompany(viewsets.ViewSet):
    def create(self, request):
        companyname = request.POST['companyname']
        if companyname  != '':
            registered = Register(companyname)
            return Response(registered)
        else:
            result = {}
            result['Message'] = 'Please input the companyname'
            return Response(result)
   
@permission_classes((permissions.AllowAny,))
class SaveFiles(viewsets.ViewSet):
    def create(self, request):
        files = request.FILES.getlist('file')
        companyname = request.POST['companyname']
        login = request.POST['FullName']
        if len(files) == 5:
            Folder = folder(login,companyname)
            for f in files:
                saved = save(login, f)
            return Response(Folder)
        else:
            result = {}
            result['Message'] = 'Please input the fields'
            return Response(result)
   
@permission_classes((permissions.AllowAny,)) 
class ModelBuilding(viewsets.ViewSet):
    def create(self, request):
        question = request.data
        gmm = model(question['FullName'],question['companyname'], question['file'])
        # deletion of folder after building gmm model #save storage
        ubm = UBMmodel('UBM', question['FullName'], question['companyname'], '')
        # deletion of folder after building gmm model #save storage
       
        current_path = path + '/' + 'UBM'
        shutil.rmtree(path + '/' + question['FullName'])
        file_list = os.listdir(current_path)
        f = [i for i in file_list if question['FullName'] in i]# to check filename loginid within ubm files
        for i in f:
            try:
                os.remove(current_path + '/' + i)
            except:
                pass
        return Response(gmm)
   
@permission_classes((permissions.AllowAny,))
class Predict(viewsets.ViewSet):
    def create(self, request):
        files = request.FILES.getlist('file')
        if len(files) > 0:
            file = files[0]
            filename = file.name
            fileext = filename.split('.')[-1:][0]
            companyname = request.POST['companyname']
            try:
                current_path = path + '/temp'
                for chunk in file.chunks():
                    Audio = AudioSegment.from_file(io.BytesIO(chunk), format=fileext)
                    normalized_audio = match_target_amplitude(Audio, -20.0)
                    file_path = os.path.join(current_path, companyname+ uuid.uuid4().hex) 
                    normalized_audio.export(file_path+'.wav', format="wav")
                file_name = file_path + '.wav'
                Sliced = AudioSlicing(file_name, companyname)
                print('asdfgthyujj', Sliced)
                prediction = predict(companyname)
                if os.path.exists(file_name):
                    os.remove(file_name)
                shutil.rmtree(path + '/' + companyname + '_sliced')
                return Response(prediction)
            except Exception as e:
                print("tttttt",e)
                result = {}
                result['Message'] = 'Please sign up'
                if os.path.exists(file_name):
                    os.remove(file_name)
                shutil.rmtree(path + '/' + companyname + '_sliced')
                return Response(result)
        else:
            result = {}
            result['Message'] = 'Please enter your voice note' 
            return Response(result)
