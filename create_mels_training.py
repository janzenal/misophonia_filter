import librosa
import numpy as np
import os.path
import os
import skimage.io
from tqdm import tqdm

def create_mels(cl, cat, seconds, overlap):
    '''
    This function creates a spectrogram of each audio slice and saves the spectrogram in a designated folder.
    '''

    # define paths for the audio files and the resulting mels
    origin_path = f"audio_files/class_{cl}/{cat}/seconds_{seconds}_overlap_{overlap}/"
    destination_path = f"mel_spectrograms/seconds_{seconds}_overlap_{overlap}/class_{cl}/{cat}/"

    # convert each slice into a mel spectrogram
    for slice in tqdm(os.listdir(origin_path)):
        if "mp3" in slice:
            audio, sr = librosa.load(origin_path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            skimage.io.imsave(destination_path + slice.replace("mp3", "png"), spectrogram_db)

classes = [0, 1]
categories = ["Train", "Test", "Validation"]

# run the code for slices of length 0.2 seconds with 0.1 seconds overlap
for cl in classes:
    for cat in categories:
        create_mels(cl, cat, 0.2, 0)
