# Author: Ben Lehrburger
# Project: Music & AI
# Script: Pitch shifting with PyTorch
# Adapted from: https://github.com/KentoNishi/torch-pitch-shift/blob/master/example.py

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    import numpy as np
    from scipy.io import wavfile
    from torch_pitch_shift import *
    from pydub import AudioSegment
    import tempfile


# Convert audio data to tensor
def to_tensor(sample):

    sample = np.reshape(sample, (sample.shape[0], 1))

    dtype = sample.dtype

    sample = torch.tensor(
        [np.swapaxes(sample, 0, 1)],  # (samples, channels) --> (channels, samples)
        dtype=torch.float32,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )

    return sample, dtype


# Shift up to target pitch
def shift_up(s, sr, dtype, num):

    up = pitch_shift(s, num, sr)
    assert up.shape == s.shape

    temp_output = tempfile.mktemp(suffix="wav")
    wavfile.write(temp_output, sr, np.swapaxes(up.cpu()[0].numpy(), 0, 1).astype(dtype))

    shifted_output = AudioSegment.from_file_using_temporary_files(temp_output, frame_rate=sr, channels=1)

    return shifted_output


# Shift down to target pitch
def shift_down(s, sr, dtype, num):

    down = pitch_shift(s, num, sr)
    assert down.shape == s.shape

    temp_output = tempfile.mktemp(suffix="wav")
    wavfile.write(temp_output, sr, np.swapaxes(down.cpu()[0].numpy(), 0, 1).astype(dtype))

    shifted_output = AudioSegment.from_file_using_temporary_files(temp_output, frame_rate=sr, channels=1)

    return shifted_output
