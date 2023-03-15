# Author: Ben Lehrburger
# Project: Music & AI
# Script: Handle input and output file paths

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    import sounddevice as sd
    from scipy.io import wavfile
    import os
    import ast


# Receive vocal input from microphone
def get_input(fs=44100, duration=5):

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    print('\nRecording...\n')
    sd.wait()

    return recording, fs


# Use an input already in directory
def bypass_input(file):

    return wavfile.read(file)


# Number a file if another with the same name exists
def enumerate_file(file_name, parent=None):

    for num in range(0, 9999):

        file = f'{file_name}{num}.wav'

        if parent:
            file = f'{parent}/{file_name}{num}.wav'

        if not os.path.exists(file):
            return file


# Retrieve stored MIDI data from prior parse
def get_stored_data(dataFile):

    with open(dataFile) as f:
        data = f.read()

    d = ast.literal_eval(data)

    return d
