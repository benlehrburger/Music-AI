import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    import sounddevice as sd
    from scipy.io import wavfile
    import os
    import ast


def get_input(fs=44100, duration=5):

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    print('\nRecording...\n')
    sd.wait()

    return recording, fs


def bypass_input(file):

    return wavfile.read(file)


def enumerate_file(file_name, parent=None):

    for num in range(0, 9999):

        file = f'{file_name}{num}.wav'

        if parent:
            file = f'{parent}/{file_name}{num}.wav'

        if not os.path.exists(file):
            return file


def get_stored_data(dataFile):

    with open(dataFile) as f:
        data = f.read()

    d = ast.literal_eval(data)

    return d
