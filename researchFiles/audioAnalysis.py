import librosa
import IPython.display as ipd
import numpy as np


def get_audio_data(filePath):

    x, sr = librosa.load(filePath)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)

    return x, sr, onset_frames


file = 'audioInputs/aivaCMin.wav'

x, sr, onset_frames = get_audio_data(file)

print(onset_frames)

onset_times = librosa.frames_to_time(onset_frames)

clicks = librosa.clicks(frames=onset_frames, sr=sr, length=len(x))

overlayedAudio = ipd.Audio(x + clicks, rate=sr)

with open('audioOutputs/clickOutput.wav', 'wb') as f:
    f.write(overlayedAudio.data)


# WITH BACKTRACKING
# Result is significantly more onsets

file = 'audioInputs/aivaCMin.wav'

y, sr = librosa.load(file)
oenv = librosa.onset.onset_strength(y=y, sr=sr)

onset_backtracked = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=True)
onset_backtracked = np.unique(onset_backtracked)

clicks = librosa.clicks(frames=onset_backtracked, sr=sr, length=len(y))

overlayedAudio = ipd.Audio(y + clicks, rate=sr)

with open('audioOutputs/clickOutput.wav', 'wb') as f:
    f.write(overlayedAudio.data)

