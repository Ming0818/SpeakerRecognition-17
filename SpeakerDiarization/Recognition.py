'''
Created on 19-Nov-2018

@author: anu
'''
import speech_recognition as sr

def recognition(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        recognized = r.recognize_google(audio)
        print(recognized)
        return recognized
    except:
        pass