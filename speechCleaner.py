import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    import noisereduce as nr
    from scipy.io import wavfile
    from pydub import AudioSegment, effects
    import numpy as np


# CLEAN AUDIO FILE NOISE
def reduce_noise(inputFile):

    rate, data = wavfile.read(inputFile)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    reduced_noise = float2pcm(reduced_noise)
    wavfile.write(inputFile, rate, reduced_noise)


def normalize_sound(inputFile):

    raw_sound = AudioSegment.from_file(inputFile)
    normalized_sound = effects.normalize(raw_sound)
    normalized_sound = float2pcm(normalized_sound)
    normalized_sound.export(inputFile)


def float2pcm(data, dtype='int16'):

    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max

    return (data * abs_max + offset).clip(i.min, i.max).astype(dtype)

