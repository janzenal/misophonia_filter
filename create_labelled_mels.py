from pydub import AudioSegment
import librosa
import pandas as pd
import numpy as np
import os.path
import os
import skimage.io
from tqdm import tqdm
import natsort

def clean_labels(file_path):
    '''
    This function cleans the label file created with Audacity from the lines that do not include useful information
    '''

    with open(file_path, "r") as f:
        lines = f.readlines()
    with open(file_path, "w") as f:
        for line in lines:
            if "smack" in line.strip("\n"):
                f.write(line)
            if "breather" in line.strip("\n"):
                f.write(line)
            if "tongue" in line.strip("\n"):
                f.write(line)
            if "nose" in line.strip("\n"):
                f.write(line)
            if "swallow" in line.strip("\n"):
                f.write(line)

def slicing_audio(audio_track, name, number, seconds):
    '''
    This function creates audio slices of a specified length in milliseconds and stores these in a designated folder.
    Each slice has attached to its name the second it starts in the entire audio segment, e.g. slice 14 is the slice
    that starts at second 14 in the audio segment. The last slice, if shorter than the specified length, is omitted.
    '''

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = int(seconds * 1000)

    # create a folder to store the slices in
    if os.path.isdir(f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/") == False:
        os.mkdir(f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/")
    if os.path.isdir(f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/{name}_{number}/") == False:
        os.mkdir(f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/{name}_{number}/")

    # loop over all timestamps at which you want to insert a cut
    for milsec in range(0, len(audio_track), milliseconds):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/{name}_{number}/{name}_{number}_slice_{int(milsec/100)}.mp3",
                format="mp3")

def create_stamp_list(path):
    '''
    This function creates a list of stamps that will be used in the subsequent step of the process of labelling the slices
    '''

    # first, create a dataframe with columns start, end, label
    df = pd.read_csv(path, names=["start", "end", "label"], delimiter="\t")

    # then, loop over each start and end entry simultaneously and append both values to a list
    # so that ultimately, we get a list of all timestamps in chronological order
    stamp_list = []
    for (stamp_start, stamp_end) in zip(df.loc[:, "start"], df.loc[:, "end"]):
        stamp_list.append(stamp_start)
        stamp_list.append(stamp_end)
    return stamp_list

def create_label_list(stamp_list, path_slices, seconds):
    '''
    This function loops over all seconds x at which a slice starts (e.g. 0, 2, 4, 6, ... ) and checks if
    any timestamp of the stamp list is included in the range x and x + 2 . If yes, the label is 1, else 0.
    First, we determine the number of slices by counting the files in the slices folder.
    Then, we loop of all starting seconds and check for a time stamp in that range.
    '''

    list_slices = os.listdir(path_slices)
    number_slices = len(list_slices)

    label_list = []
    for i in range(0, number_slices):
        '''
        In each iteration i the test number is changed to something greater than 0 if there is at least one time stamp
        that falls in the range of i and i+2.
        '''
        test_number = 0
        for element in stamp_list:
            if element > (i * seconds) and element < ((i * seconds) + seconds):
                test_number += 1
        if test_number == 0:
            label_list.append(0)
        else:
            label_list.append(1)
    return label_list

def delete_zeros(label_list, name, number, seconds):
    '''
    This function samples down both the list of labels and the list of slices to get a balanced amount in both classes.
    '''

    # first, determine the number of 0's to be deleted
    n_to_delete = label_list.count(0) - label_list.count(1)

    # k counts the times a 0 was deleted. If k reaches the number of 0's to be deleted, the loop stops.
    k = 0

    # j is the index of the current element to be checked. It moves one up each time a 1 was encountered.
    j = 0

    for i in range(len(label_list)):
        if label_list[j] == 1:
            j += 1
        elif label_list[j] == 0:
            label_list.pop(j)
            os.remove(f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/{name}_{number}/{name}_{number}_slice_{round((i * seconds) * 10)}.mp3")
            k += 1
            if k == n_to_delete:
                break
    return label_list

def extend_data(path, label_list, cat):
    '''
    This function creates mel spectrograms and adds them to the corresponding classes.
    '''

    # define path for the mels
    destination_path = f"mel_spectrograms_manually_labelled/{cat}/"

    # convert each slice into a mel spectrogram and store it in the right category folder
    files = os.listdir(path)
    for i, slice in tqdm(enumerate(natsort.natsorted(files))):
        if "mp3" in slice:
            audio, sr = librosa.load(path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            skimage.io.imsave(destination_path + f"class_{label_list[i]}/" + slice.replace("mp3", "png"), spectrogram_db)

def add_new_slices_and_labels(name, number, seconds, cat):
    '''
    This function puts all the steps together for extending both the slices and the labels
    '''

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files_manually_labelled/{name}/{name}_{number}.mp3"
    path_labels = f"label_collections/{name}/{name}_{number}.txt"

    # loading the audio file from the specified path
    audio_file = AudioSegment.from_mp3(path_audio)

    # cleaning the label file of unwanted lines (that are created during the audio labelling process
    clean_labels(path_labels)

    # slicing the audio file and storing it in a designated folder
    slicing_audio(audio_file, name, number, seconds)

    # creating a variable for the created folder with the slices
    path_slices = f"audio_files_manually_labelled/{name}/{name}_slices_{seconds}/{name}_{number}/"

    # create the stamp list
    stamp_list = create_stamp_list(path_labels)

    # creates the label list for the audio slices
    label_list = create_label_list(stamp_list, path_slices, seconds)

    # creates new balanced label list and deletes the corresponding slices
    new_label_list = delete_zeros(label_list, name, number, seconds)

    # extend the data with new slices
    extend_data(path_slices, new_label_list, cat)

# specify in the arguments:
# the name_surname
# number of audio file of that source
# the slice length in seconds
# the category the slices belong to (train, test or validation)
add_new_slices_and_labels("Steve_Brunton", 1, 0.2, "Validation")