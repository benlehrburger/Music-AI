from pedalboard import Pedalboard, Reverb, Distortion, GSMFullRateCompressor
from pedalboard.io import AudioFile

read_in_file = 'audioOutputs/output_with_samples_on_beat.wav'

# Make a Pedalboard object, containing multiple audio plugins:
board = Pedalboard([Distortion(drive_db=15), Reverb(room_size=0.05)])

# Open an audio file for reading, just like a regular file:
with AudioFile(read_in_file) as f:
    # Open an audio file to write to:
    with AudioFile('pedalboard_test_output.wav', 'w', f.samplerate, f.num_channels) as o:
        # Read one second of audio at a time, until the file is empty:
        while f.tell() < f.frames:
            chunk = f.read(int(f.samplerate))

            # Run the audio through our pedalboard:
            effected = board(chunk, f.samplerate, reset=False)

            # Write the output to our output file:
            o.write(effected)