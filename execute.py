# Author: Ben Lehrburger
# Project: Music & AI
# Script: Main executable function

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    from autotuner import autotune
    from audioInput import bypass_input, enumerate_file
    from midiParser import bypass_parse, parse_midi_track
    from speechCleaner import reduce_noise
    from speechRecognition import recognition_split
    from assembleVocalTrack import assemble_vocal_track
    from overlayTracks import overlay
    from scipy.io import wavfile
    import os
    import pathlib


while True:

    try:

        input_file = input('Please enter the name of your vocal input file: ')

        global_path = pathlib.Path(__file__).parent.resolve()
        audio_output_path = 'Audio Output'

        if input_file == 'example':

            backtrack_file_path = 'Audio Input/Example/backtrack.wav'
            vocal_timestamps, vocal_key = bypass_parse(sample=2)
            raw_input_sr, raw_input_data = wavfile.read('Audio Input/Example/raw_vocal_input.wav')
            print('Got input data from example')

        else:

            backtrack_file = input('Please enter the name of your backtrack file: ')
            melody_file = input('Please enter the name of your melody file: ')

            backtrack_file_path = 'Audio Input/' + backtrack_file
            melody_file_path = 'Audio Input/' + melody_file
            input_file_path = 'Audio Input/' + input_file

            raw_input_sr, raw_input_data = wavfile.read(input_file_path)
            print('Received vocal input data')
            print('Parsing new MIDI file – this can take several minutes')
            vocal_timestamps, vocal_key = parse_midi_track(melody_file_path)
            print('Parsed MIDI file')

        tuned_input_data, tuned_input_sr = autotune(vocal_key, raw_input_data, raw_input_sr)
        augmented_vocal_path = enumerate_file('augmented_vocals', parent=audio_output_path)
        wavfile.write(augmented_vocal_path, tuned_input_sr, tuned_input_data)
        print('Autotuned vocal input')

        reduce_noise(augmented_vocal_path)
        print('Normalized and cleaned vocal input')

        sample_metadata = recognition_split(augmented_vocal_path)
        print('Split input file into samples')

        vocal_melody_path = enumerate_file('vocalMelody', parent=audio_output_path)
        assemble_vocal_track(vocal_timestamps, sample_metadata, vocal_melody_path)
        print('Created melody track')

        final_path = enumerate_file('Composition', parent=audio_output_path)
        os.remove(augmented_vocal_path)

        overlay(vocal_melody_path, backtrack_file_path, final_path, vocalBoost=10)
        os.remove(vocal_melody_path)

        print('Completed vocal sample insertion!')

        break

    except:
        break
