# Author: Ben Lehrburger
# Project: Music & AI
# Script: Autotune an audio track to a given key
# Adapted from: https://thewolfsound.com/how-to-auto-tune-your-voice-with-python/

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    from functools import partial
    import numpy as np
    import scipy.signal as sig
    import psola
    from librosa import key_to_degrees, hz_to_midi, midi_to_hz, note_to_hz, pyin
    import librosa.display


SEMITONES_IN_OCTAVE = 12


# Return the pitch classes (degrees) that correspond to the given scale
def degrees_from(scale: str):

    degrees = key_to_degrees(scale)
    degrees = np.concatenate((degrees, [degrees[0] + SEMITONES_IN_OCTAVE]))

    return degrees


# Return the pitch closest to the current voice that belongs to the given scale
def closest_pitch_from_scale(f0, scale):

    if np.isnan(f0):
        return np.nan

    degrees = degrees_from(scale)
    midi_note = hz_to_midi(f0)

    degree = midi_note % SEMITONES_IN_OCTAVE
    degree_id = np.argmin(np.abs(degrees - degree))
    degree_difference = degree - degrees[degree_id]
    midi_note -= degree_difference

    return midi_to_hz(midi_note)


# Map each pitch input to the closest pitch in the given scale
def map_closest_pitch(f0, scale):

    sanitized_pitch = np.zeros_like(f0)
    for i in np.arange(f0.shape[0]):
        sanitized_pitch[i] = closest_pitch_from_scale(f0[i], scale)

    smoothed_sanitized_pitch = sig.medfilt(sanitized_pitch, kernel_size=11)
    smoothed_sanitized_pitch[np.isnan(smoothed_sanitized_pitch)] = \
        sanitized_pitch[np.isnan(smoothed_sanitized_pitch)]

    return smoothed_sanitized_pitch


# Pitch track and shift to scale
def tune(audio, sr, correction_function):

    frame_length = 2048
    hop_length = frame_length // 4

    fmin = note_to_hz('C2')
    fmax = note_to_hz('C7')

    # Pitch tracking using the PYIN algorithm
    f0, voiced_flag, voiced_probabilities = pyin(audio,
                                                     frame_length=frame_length,
                                                     hop_length=hop_length,
                                                     sr=sr,
                                                     fmin=fmin,
                                                     fmax=fmax)

    corrected_f0 = correction_function(f0)

    # Pitch-shifting using the PSOLA algorithm
    return psola.vocode(audio, sample_rate=int(sr), target_pitch=corrected_f0, fmin=fmin, fmax=fmax)


# Main executable function
def autotune(scale, inputData, inputSR):

    y, sr = inputData, inputSR

    if y.ndim > 1:
        y = y[0, :]

    correction_function = partial(map_closest_pitch, scale=scale)

    pitch_corrected_y = tune(y, sr, correction_function)

    return pitch_corrected_y, sr
