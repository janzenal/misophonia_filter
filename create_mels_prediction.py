from tqdm import tqdm
import os
import librosa
import numpy as np
import skimage.io

def create_mels(name, number, seconds, overlap):
    '''
    This function creates a mel-spectrogram of each slice and saves the mel in a designated folder.
    '''

    # define paths for the audio files and the resulting mels
    origin_path = f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/"
    if os.path.isdir(f"mel_spectrograms/seconds_{seconds}_overlap_{seconds}/for_prediction/{name}_{number}/") == False:
        os.mkdir(f"mel_spectrograms/seconds_{seconds}_overlap_{seconds}/for_prediction/{name}_{number}/")
    destination_path = f"mel_spectrograms/seconds_{seconds}_overlap_{seconds}/for_prediction/{name}_{number}/"

    # convert each slice into a mel spectrogram
    for i, slice in tqdm(enumerate(os.listdir(origin_path))):
        if "mp3" in slice:
            audio, sr = librosa.load(origin_path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            skimage.io.imsave(destination_path + slice.replace("mp3", "png"), spectrogram_db)

# apply function with the following parameters:
# name of the audio file
# which number of that audio file
# the slice length
# how much overlap between the slices
create_mels("Recording", 1, 0.2, 0)