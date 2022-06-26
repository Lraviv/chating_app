"handles the speaking and recognizing"
import os
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import playsound
#import pyaudio



def recognize():
    #recognize what user say
    speak("say something please")
    # initiate recording
    r = sr.Recognizer()

    with sr.Microphone() as source:
        aud_text = r.listen(source)
        # try to recognize what user said
        try:
            text = r.recognize_google(aud_text)
            print("converting audio to text...")
            print("user said:" + text)
            speak("user said:" + text)
            return text

        except:
            text = "sorry,I didn't understand you"
            speak(text)
            print(text)
            return text

def speak(audio):
    tts = gTTS(text=audio, lang='iw')  # text to speech(voice)
    r = "speak_" + datetime. now(). strftime("%Y_%m_%d-%I-%M-%S_%p")
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    playsound.playsound(audio_file)  # play the audio file
    print(f"system: {audio}")  # print what app said
    os.remove(audio_file)  # remove audio file

print(recognize())