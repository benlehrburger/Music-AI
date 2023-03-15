# Author: Ben Lehrburger
# Project: Music & AI
# Script: Split audio file into individual words

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    from vosk import Model, KaldiRecognizer, SetLogLevel
    from scipy.io import wavfile
    import wave
    import json
    import os


# Retrieve the timestamps at which words occur in an audio file
def get_vocal_timestamps(wav_path):

    SetLogLevel(-1)

    model = Model('voskModel')
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []

    while True:

        data = wf.readframes(4000)

        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    structured_data = []
    words = []

    for entry in results[0]['result']:
        words.append(entry['word'])
        structured_data.append([entry['word'], entry['start'], entry['end']])

    return structured_data, words


# Split an audio file at the timestamps of word onset and offset
def recognition_split(inputPath):

    word_timestamps = get_vocal_timestamps(inputPath)[0]

    vocal_rate, vocal_data = wavfile.read(inputPath)
    sample_metadata = []

    split_audio_path = 'Audio Output/Samples'

    sample_counter = 0

    for stamp in word_timestamps:

        mutable_vocal_data = vocal_data.copy()
        word, start_time, end_time = stamp[0], stamp[1], stamp[2]
        start_frame, end_frame = int(vocal_rate * start_time), int(vocal_rate * end_time)

        word_data = mutable_vocal_data[start_frame:end_frame]

        fileName = 'sample' + f'{sample_counter}.wav'
        sample_path = os.path.join(split_audio_path, fileName)
        wavfile.write(sample_path, vocal_rate, word_data)
        sample_metadata.append(sample_path)

        sample_counter += 1

    return sample_metadata
