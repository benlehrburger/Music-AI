import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

    from pitchShifter import *
    from pydub import AudioSegment
    import tempfile
    from librosa import load
    from librosa import effects


def pitch_shift(pitch_change, sample, sample_rate):

    if pitch_change > 0:

        slowed_sample, dtype = to_tensor(sample)
        temp = shift_up(slowed_sample, sample_rate, dtype, pitch_change)

        return temp

    elif pitch_change < 0:

        slowed_sample, dtype = to_tensor(sample)
        temp = shift_down(slowed_sample, sample_rate, dtype, pitch_change)

        return temp

    else:

        temp_output = tempfile.mktemp(suffix="wav")
        wavfile.write(temp_output, sample_rate, sample)
        silent_output = AudioSegment.from_file_using_temporary_files(temp_output, frame_rate=sample_rate, channels=1)

        return silent_output


def apply_fadeout(data, sr, proportional_fade=1.0):

    length_of_sample = len(data) / sr
    end = data.shape[0]
    duration_of_fadeout = length_of_sample * proportional_fade
    data_length_of_fadeout = int(duration_of_fadeout * sr)
    start = end - data_length_of_fadeout
    fade_curve = np.linspace(1.0, 0.0, data_length_of_fadeout)
    data[start:end] = data[start:end] * fade_curve

    return data


def get_next_sample(sample_counter, samples):

    current_sample_index = sample_counter % len(samples)
    current_sample = samples[current_sample_index]

    sample_data, sample_rate = load(current_sample)
    sample_length = len(sample_data) / sample_rate

    return sample_data, sample_rate, sample_length


def compress_or_expand(sample_length, note_duration, sample_data):

    rate_of_change = sample_length / note_duration
    time_modulated_sample = effects.time_stretch(sample_data, rate=rate_of_change)

    return time_modulated_sample


def cut_off(note_duration, sample_rate, sample_data, proportional_fade=0.1):

    cutoff = int(note_duration * sample_rate)
    time_modulated_sample = sample_data[0:cutoff]
    time_modulated_sample = apply_fadeout(time_modulated_sample, sample_rate, proportional_fade=proportional_fade)

    return time_modulated_sample


def assemble_vocal_track(track_data, samples, outputPath):

    track_keys = list(track_data.keys())

    melody_tracks = []
    sample_counter = 0

    for time_stamp, stamp_data in track_data.items():

        current_stamp_index = track_keys.index(time_stamp)

        if current_stamp_index < len(track_keys) - 1:

            note_duration, note_pitch = stamp_data[0], stamp_data[1]
            next_stamp = track_keys[current_stamp_index + 1]

            if note_duration != 0:

                sample_data, sample_rate, sample_length = get_next_sample(sample_counter, samples)

                time_modulated_sample = None

                if abs(sample_length - note_duration) <= 0.1:
                    time_modulated_sample = compress_or_expand(sample_length, note_duration, sample_data)

                else:

                    if sample_length > note_duration:
                        time_modulated_sample = cut_off(note_duration, sample_rate, sample_data)

                    elif sample_length < note_duration:

                        greater_than_note = False
                        current_data = np.array([])
                        adjustment_per_sample = 0
                        total_duration = sample_length
                        num_consecutive_samples = 1
                        sample_counter_copy = sample_counter

                        while not greater_than_note:

                            sample_counter_copy += 1
                            temp_data, temp_rate, temp_length = get_next_sample(sample_counter_copy, samples)
                            total_duration += temp_length
                            num_consecutive_samples += 1

                            if total_duration >= note_duration:

                                plus_one = total_duration - note_duration
                                minus_one = abs(total_duration - temp_length - note_duration)

                                if plus_one < minus_one:

                                    adjustment_per_sample += (note_duration - total_duration) / num_consecutive_samples
                                    greater_than_note = True

                                else:

                                    num_consecutive_samples -= 1
                                    total_duration -= temp_length
                                    sample_counter_copy -= 1
                                    adjustment_per_sample += (note_duration - total_duration) / num_consecutive_samples
                                    greater_than_note = True

                        for sample in range(0, num_consecutive_samples):

                            sample_data, sample_rate, sample_length = get_next_sample(sample_counter, samples)
                            adjusted_sample_duration = sample_length + adjustment_per_sample
                            time_adjusted_sample = compress_or_expand(sample_length, adjusted_sample_duration, sample_data)
                            current_data = np.concatenate((current_data, time_adjusted_sample), axis=0)
                            sample_counter += 1

                            if sample_counter > sample_counter_copy:
                                sample_counter -= 1

                        time_modulated_sample = current_data

                temp_output = tempfile.mktemp(suffix="wav")
                wavfile.write(temp_output, int(sample_rate), time_modulated_sample)
                output = AudioSegment.from_file_using_temporary_files(temp_output, frame_rate=sample_rate, channels=1)
                melody_tracks.append(output)

                sample_counter += 1

            if time_stamp + note_duration < next_stamp:

                time_void = next_stamp - (time_stamp + note_duration)

                if time_void >= 0.8:
                    sample_counter = 0
                    verse_samples = 0

                # if time_void >= 5:
                #
                #     sample_counter = 0
                #     leftover_samples = verse_samples % len(samples)
                #
                #     if leftover_samples != 0:
                #
                #         index = leftover_samples + silences_per_sample_iter
                #         verse_track = verse_track[0:-index]
                #         melody_tracks.append(verse_track)
                #         verse_track = []
                #         verse_samples = 0
                #         silences_per_sample_iter = 0
                #
                #     else:
                #
                #         melody_tracks.append(verse_track)
                #         verse_track = []
                #         verse_samples = 0
                #         silences_per_sample_iter = 0

                silence = AudioSegment.silent(duration=time_void * 1000)

                # if verse_samples % len(samples) == 0:
                #     silences_per_sample_iter = 0

                melody_tracks.append(silence)

        else:
            break

    vocal_track = AudioSegment.empty()

    for track in melody_tracks:
        vocal_track += track

    vocal_track.export(outputPath, format='wav')
