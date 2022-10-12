from fileinput import filename
from flask import Flask ,jsonify, redirect , url_for , render_template , request ,Response
import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
from pydub.silence import split_on_silence
import speech_recognition as sr
import shutil
from werkzeug.utils import secure_filename
def import_file():
    root = tk.Tk()
    filename = filedialog.askopenfilename(filetypes=[("audio","*.wav *.ogg *.mp3 *.aac *.flac *.alac *.AIFF")],title = 'Choose a File')
    root.destroy()
    print(filename)
    return filename

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """ 
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 200,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=200,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    return whole_text
    

def transcript(filename):
   
   
    if os.path.splitext(filename)[1] != ".wav":
        sound_file=os.path.splitext(filename)[0]+".wav"
        sound = AudioSegment.from_file(filename)
        out_ =sound.export(sound_file, format="wav")
        
        out_.close() 
    else:
        sound_file=filename
        
    output=get_large_audio_transcription(sound_file)

    return output


app=Flask(__name__)

@app.route("/",methods=["POST","GET"])


def convert1():
    if request.method=="POST": 
        print("hhhhhhhhhhhhhhhh")
        f = request.files["audio_file"] 
        print(f) 
        f.save(secure_filename(f.filename))
        res   = transcript((secure_filename(f.filename)))
    
        print(res)
        return Response(res)
    else:
        return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)