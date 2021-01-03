import librosa
import numpy as np
import os.path
import os
import random
from tqdm import tqdm
import skimage.io

def noise(data, noise_factor):
    """
    This function adds noise to an audio file
    """
    noise = np.random.randn(len(data))
    augmented_data = data + noise_factor * noise
    # Cast back to same data type
    augmented_data = augmented_data.astype(type(data[0]))
    return augmented_data

def shift(data, sampling_rate, shift_max, shift_direction):
    """
    This function shifts the audio file
    """
    shift = np.random.randint(sampling_rate * shift_max)
    if shift_direction == 'right':
        shift = -shift
    elif shift_direction == 'both':
        direction = np.random.randint(0, 2)
        if direction == 1:
            shift = -shift
    augmented_data = np.roll(data, shift)
    # Set to silence for heading/ tailing
    if shift > 0:
        augmented_data[:shift] = 0
    else:
        augmented_data[shift:] = 0
    return augmented_data

def pitch(data, sampling_rate, pitch_factor):
    """
    This function changes the pitch of the audio file by a specified pitch factor
    """
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)


def manipulate(file):
    """
    This function applies all three augmentation methods to an audio file and creates a mel-spectrogram of it.
    """
    audio, sr = librosa.load(file)

    # add noise
    noise_factor = random.uniform(0.0001, 0.02)
    noise_audio = noise(audio, noise_factor)

    # shift
    shift_max = round(random.uniform(0.05, 0.15), 2)
    shift_direction = random.choice(["both", "right"])
    shift_audio = shift(noise_audio, 22050, shift_max, shift_direction)

    # change pitch
    n1 = round(random.uniform(-2, -0.2), 2)
    n2 = round(random.uniform(0.2, 2), 2)
    res = np.stack((n1, n2))
    pitch_factor = np.random.choice(res)
    pitch_audio = pitch(shift_audio, 22050, pitch_factor)

    spectrogram = librosa.feature.melspectrogram(y=pitch_audio, sr=sr)
    spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
    return spectrogram_db

def create_augmented_mels(cl, seconds, overlap):
    '''
    This function saves all augmented mel-spectrograms in a designated folder.
    '''

    # define paths for the audio files and the resulting mels
    origin_path = f"audio_files/class_{cl}/Train/seconds_{seconds}_overlap_{overlap}/"
    destination_path = f"mel_spectrograms/seconds_{seconds}_overlap_{overlap}/Train/class_{cl}/"

    # convert each slice into a mel spectrogram
    for slice in tqdm(os.listdir(origin_path)):
        if "mp3" in slice:
            manipulated_mel = manipulate(origin_path + slice)
            skimage.io.imsave(destination_path + "aug_" + slice.replace("mp3", "png"), manipulated_mel)

create_augmented_mels(1, 0.2, 0)
