import fleep
import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

def import_file():
    root = tk.Tk()
    filename = filedialog.askopenfilename()
    root.destroy()
    print(filename)
    return filename

r = sr.Recognizer()

filename=import_file()
with open(filename, "rb") as file:
    info = fleep.get(file.read(128))
    
if info.extension[0] != "wav":
    sound_file=os.path.splitext(filename)[0]+".wav"
    sound = AudioSegment.from_file(filename)
    out_ =sound.export(sound_file, format="wav")
    out_.close()
    
with sr.AudioFile(sound_file) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)
    
if os.path.exists(sound_file):
    os.remove(sound_file)    