from pycomposer.gancomposable._torch.conditional_gan_composer import ConditionalGANComposer
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import torch

logger = getLogger("pygan")
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

ctx = "cuda:0" if torch.cuda.is_available() else "cpu"

print('Set up dependencies...')

gan_composer = ConditionalGANComposer(
    # `list` of Midi files to learn.
    midi_path_list=[
        "audioInputs/electronic-sample.midi"
    ],
    # Batch size.
    batch_size=5,
    # The length of sequence that LSTM networks will observe.
    seq_len=8,
    # Learning rate in `Generator` and `Discriminator`.
    learning_rate=1e-10,
    # Time fraction or time resolution (seconds).
    time_fraction=0.5,
    # Context-manager that changes the selected device.
    ctx=ctx
)

print('Read input data...')

gan_composer.learn(
    # The number of training iterations.
    iter_n=5,
    # The number of learning of the `discriminator`.
    k_step=10
)

print('Successfully trained model...')

gan_composer.compose(
    # Path to generated MIDI file.
    file_path="gan-output.mid",
    # Mean of velocity.
    # This class samples the velocity from a Gaussian distribution of
    # `velocity_mean` and `velocity_std`.
    # If `None`, the average velocity in MIDI files set to this parameter.
    velocity_mean=None,
    # Standard deviation(SD) of velocity.
    # This class samples the velocity from a Gaussian distribution of
    # `velocity_mean` and `velocity_std`.
    # If `None`, the SD of velocity in MIDI files set to this parameter.
    velocity_std=None
)

print('Finished composition...')
