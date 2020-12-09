import os.path
import os
from pydub import AudioSegment
import numpy as np
import librosa


def create_label_list(path_slices_0, path_slices_1, cat, seconds):
    '''
    This function creates the labels for both classes.
    '''

    list_slices_0 = os.listdir(path_slices_0)
    list_slices_1 = os.listdir(path_slices_1)
    number_slices_0 = len(list_slices_0)
    number_slices_1 = len(list_slices_1)

    label_list_0 = [0 for i in range(number_slices_0)]
    label_list_1 = [1 for i in range(number_slices_1)]

    label_list = label_list_0 + label_list_1

    with open(f'labels/seconds_{seconds}_shuffled/labels_{cat}.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in label_list)
        
def covert_data(path_slices_0, path_slices_1, cat, seconds, overlap):
    '''
    This function creates a spectrogram of each slice and saves the result as a numpy array in data.txt.
    '''

    # collect all the slices in a list
    data_list = []

    if os.path.exists(path_slices_0 + "wav_compressed/") == False:
        os.mkdir(path_slices_0 + "wav_compressed/")
    if os.path.exists(path_slices_1 + "wav_compressed/") == False:
        os.mkdir(path_slices_1 + "wav_compressed/")

    # convert each slice into a mel spectrogram and append it to a list
    for i, slice in enumerate(os.listdir(path_slices_0)):
        if "mp3" in slice:
            if i % 2 == 0:
                wav_path = slice.replace("mp3", "wav")

                # convert wav to mp3
                sound = AudioSegment.from_mp3(path_slices_0 + slice)
                sound = sound.set_frame_rate(16000)
                sound.export(path_slices_0 + "wav_compressed/" + wav_path, format="wav")
                wav_file, sr = librosa.load(path_slices_0 + "wav_compressed/" + wav_path)
                data_list.append(wav_file)

    for i, slice in enumerate(os.listdir(path_slices_1)):
        if "mp3" in slice:
            if i % 2 == 0:
                wav_path = slice.replace("mp3", "wav")

            # convert wav to mp3
                sound = AudioSegment.from_mp3(path_slices_1 + slice)
                sound = sound.set_frame_rate(16000)
                sound.export(path_slices_1 + "wav_compressed/" + wav_path, format="wav")
                wav_file, sr = librosa.load(path_slices_1 + "wav_compressed/" + wav_path)
                data_list.append(wav_file)

    # convert the list to a numpy array
    array = np.array(data_list)

    # save the array to a txt file
    file = open(f"data_wav_compressed/seconds_{seconds}_overlap_{overlap}/data_{cat}.txt", "w")
    for row in array:
        np.savetxt(file, row)

def shape(path_slices, cat, seconds, overlap):
    '''
    This function prints the current shape of the data array and the distribution of 1's and 0's.
    It also shows the class distribution.
    '''

    # get the image size for reshaping the data file by picking out the first file in the slice folder
    k = 0
    for slice in os.listdir(path_slices):
        if "mp3" in slice:
            audio, sr = librosa.load(path_slices + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            width = spectrogram_db.shape[1]
            height = spectrogram_db.shape[0]
            k +=1
        if k > 0:
            break

    # loads and prints the shape of the data array
    data = np.loadtxt(f"data/seconds_{seconds}_overlap_{overlap}/data_{cat}.txt")
    data = data.reshape(-1, height, width)
    print(f"The shape of your data is {data.shape}.")



def create_data_and_labels(cat, seconds):
    '''
    This function puts all the steps together for creating both the data and the labels.
    '''

    path_slices_0 = f"audio_files/class_0/{cat}/seconds_{seconds}_shuffled/wav_compressed/"
    path_slices_1 = f"audio_files/class_1/{cat}/seconds_{seconds}_shuffled/wav_compressed/"

    # creates labels
    create_label_list(path_slices_0, path_slices_1, cat, seconds)

    # creates data
    #covert_data(path_slices_0, path_slices_1, cat, seconds, overlap)

    # printing the shape of the data
    #shape(path_slices_0, cat, seconds, overlap)

# arguments: category
def perform(seconds):
    create_data_and_labels("Test", seconds)
    create_data_and_labels("Validation", seconds)
    create_data_and_labels("Train", seconds)

perform(0.2)