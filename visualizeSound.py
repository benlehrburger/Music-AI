import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    from scipy.io.wavfile import read
    import matplotlib.pyplot as plt


path = "insert_your_wave_file_here.wav"

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

input_data = read(path)
audio = input_data[1]

plt.plot(audio)
plt.ylabel("Amplitude")
plt.xlabel("Time")
plt.show()

