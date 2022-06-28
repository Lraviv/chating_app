"handles the speaking and recognizing"
import os
import time

import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
from pygame import mixer


class Speech():
    def __init__(self):
        self.audio = ''

    def recognize(self):
        # recognize what user say
        self.speak("say something please")
        # initiate recording
        r = sr.Recognizer()

        with sr.Microphone() as source:
            aud_text = r.listen(source)
            # try to recognize what user said
            try:
                text = r.recognize_google(aud_text)
                print("converting audio to text...")
                print("user said:" + text)
                self.speak("user said:" + text)
                return text

            except:
                text = "sorry,I didn't understand you"
                self.speak(text)
                print(text)
                return text

    def speak(self, audio):
        # receives text {audio} and makes an audio play (mp3)
        mixer.init()
        tts = gTTS(text=audio, lang='iw')  # text to speech(voice)
        audio_file = "audiospeak_" + datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p") + '.mp3'
        tts.save(audio_file)  # save as mp3
        mixer.music.load(audio_file)
        mixer.music.play()  # play the audio file
        print(f"[SYSTEM] {audio}")  # print what app said
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        mixer.quit()
        os.remove(audio_file)  # remove audio file



