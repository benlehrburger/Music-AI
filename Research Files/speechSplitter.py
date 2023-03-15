import librosa
import numpy as np
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence


# Split speech with onset detection
def onset_detect(trialIdentifier):

    y, sr = librosa.load(f'audioOutputs/output_pitch_corrected_{trialIdentifier}.wav')

    oenv = librosa.onset.onset_strength(y=y, sr=sr)

    onset_backtracked = librosa.onset.onset_detect(onset_envelope=oenv, backtrack=True)
    onset_backtracked = np.unique(onset_backtracked)

    time_stamp = 0
    too_short_cutoff = 15

    while time_stamp < len(onset_backtracked) - 1:

        if onset_backtracked[time_stamp + 1] - onset_backtracked[time_stamp] < too_short_cutoff:
            onset_backtracked = np.delete(onset_backtracked, time_stamp + 1)

        time_stamp += 1

    onset_times = librosa.frames_to_time(onset_backtracked)
    onset_times = np.append(onset_times, len(y)/sr)

    time_stamp = 0
    while time_stamp < len(onset_times) - 1:

        audio_segment = AudioSegment.from_wav(f'audioOutputs/output_pitch_corrected_{trialIdentifier}.wav')
        t1 = onset_times[time_stamp] * 1000
        t2 = onset_times[time_stamp + 1] * 1000
        audio_segment = audio_segment[t1:t2]
        audio_segment.export(f'audioOutputs/vocalSegments/trial_{trialIdentifier}_chunk{time_stamp}.wav', format="wav")
        time_stamp += 1


def silent_split(trialIdentifier):

    path = f'audioOutputs/normal_clean_pitch_corrected_{trialIdentifier}.wav'

    sound_file = AudioSegment.from_wav(path)
    audio_chunks = split_on_silence(sound_file,
                                    # must be silent for at least half a second
                                    min_silence_len=10,

                                    # consider it silent if quieter than -16 dBFS
                                    silence_thresh=-100
                                    )

    for i, chunk in enumerate(audio_chunks):
        out_file = "splitAudio/chunk{0}.wav".format(i)
        print("exporting", out_file)
        chunk.export(out_file, format="wav")
