import os.path
import os
from pydub import AudioSegment
import numpy as np
from tqdm import tqdm



def create_data(path_slices_0, path_slices_1, cat, seconds, overlap):
    '''
    This function creates a spectrogram of each slice and saves the result as a numpy array in data.txt.
    '''

    # collect all the slices in a list
    data_list = []

    if os.path.exists(path_slices_0) == False:
        os.mkdir(path_slices_0)
    if os.path.exists(path_slices_1) == False:
        os.mkdir(path_slices_1)

    # load each slice into a numpy array
    for i, slice in tqdm(enumerate(os.listdir(path_slices_1))):
        if "mp3" in slice:

            audio = AudioSegment.from_mp3(path_slices_1 + slice)

            if audio.channels == 2:
                audio = audio.set_channels(1)

            array = np.array(audio.get_array_of_samples())
            if array.shape[0] < 9600:
                pad = np.zeros((9600 - array.shape[0],))
                array = np.concatenate((array, pad), axis=0)
            data_list.append(array)

            if i % 1000 == 0:
                array = np.array(data_list)
                np.save(f"data_mp3/seconds_{seconds}_overlap_{overlap}/{cat}_1/data_{int(i/1000)}.npy", array)
                data_list = []

    for i, slice in tqdm(enumerate(os.listdir(path_slices_0))):
        if "mp3" in slice:

            audio = AudioSegment.from_mp3(path_slices_0 + slice)

            if audio.channels == 2:
                audio = audio.set_channels(1)

            array = np.array(audio.get_array_of_samples())
            if array.shape[0] < 9600:
                pad = np.zeros((9600 - array.shape[0],))
                array = np.concatenate((array, pad), axis=0)
            data_list.append(array)

            if i % 1000 == 0:
                array = np.array(data_list)
                np.save(f"data_mp3/seconds_{seconds}_overlap_{overlap}/{cat}_0/data_{i/1000}.npy", array)
                data_list = []

    # convert the list to a numpy array
    array = np.array(data_list)

    # save numpy array to a npy file
    np.save(f"data_mp3/seconds_{seconds}_overlap_{overlap}/data_{cat}.npy", array)



def create_data_and_labels(cat, seconds, overlap):
    '''
    This function puts all the steps together for creating both the data and the labels.
    '''

    path_slices_0 = f"audio_files/class_0/{cat}/seconds_{seconds}_overlap_{overlap}/"
    path_slices_1 = f"audio_files/class_1/{cat}/seconds_{seconds}_overlap_{overlap}/"

    # creates data
    create_data(path_slices_0, path_slices_1, cat, seconds, overlap)

# arguments: category
def perform(seconds, overlap):
    create_data_and_labels("Validation", seconds, overlap)
    #create_data_and_labels("Test", seconds, overlap)
    #create_data_and_labels("Train", seconds, overlap)

perform(0.2, 0.1)