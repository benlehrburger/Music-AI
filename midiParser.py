# Author: Ben Lehrburger
# Project: Music & AI
# Script: Convert MIDI file into dictionary of timestamp values

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    from mido import MidiFile
    import time


# Get the key of MIDI data
def parse_key(key):

    if 'm' in key:
        return key.replace("m", ":min")

    else:
        return key + ":maj"


# Record timestamps of note-on and note-off and pitch at each step
def parse_midi_track(inputPath):

    vocalTrack = MidiFile(inputPath)

    vocal_data = vocalTrack.tracks[0]
    key_signature = None

    for msg in vocal_data:

        if msg.type == 'key_signature':
            key_signature = parse_key(msg.key)

    time_stamps = {}
    time_stamps[0] = [0, 0]
    start_time = 0
    global_start = time.time()
    current_note = None

    for msg in vocalTrack:

        if msg.type == 'note_on':

            current_note = msg.note
            start_time = time.time()

        time.sleep(msg.time)

        if msg.type == 'note_off':

            end_time = time.time()
            elapsed_time = end_time - start_time
            contextual_stamp = start_time - global_start
            note_data = [elapsed_time, current_note]
            time_stamps[contextual_stamp] = note_data

    total_time_end = time.time()
    end_of_track = total_time_end - global_start
    time_stamps[end_of_track] = [0, 0]

    return time_stamps, key_signature


# Run the example and use pre-stored data
def bypass_parse(sample=None):

    data = {0: [0, 0], 39.0: [0.8, 74], 39.8: [0.4, 71], 40.2: [0.25, 76],
            43.0: [0.8, 74], 43.8: [0.65, 76], 44.45: [1.25, 71],

            46.5: [0.8, 74], 47.3: [0.4, 71], 47.7: [0.25, 76],
            50.5: [0.8, 74], 51.3: [0.65, 76], 51.95: [1.25, 71],

            85.0: [0.8, 74], 85.8: [0.4, 71], 86.2: [0.25, 76],
            89.0: [0.8, 74], 89.8: [0.65, 76], 90.45: [1.25, 71],

            92.5: [0.8, 74], 93.3: [0.4, 71], 93.7: [0.25, 76],
            96.5: [0.8, 74], 97.3: [0.65, 76], 97.95: [1.25, 71],

            112.8: [0.8, 74], 113.6: [0.65, 76], 114.25: [1.25, 71],

            115.5: [0.8, 74], 116.3: [0.4, 71], 116.7: [0.25, 76],
            119.5: [0.8, 74], 120.3: [0.65, 76], 120.95: [1.25, 71],

            123.0: [0.8, 74], 123.8: [0.4, 71], 124.2: [0.25, 76],
            127.0: [0.8, 74], 127.8: [0.65, 76], 128.45: [1.25, 71],

            129.7: [0.8, 74], 130.5: [0.65, 76], 131.15: [1.25, 71]}

    key = "C:maj"

    return data, key
