from pydub import AudioSegment
import librosa
import pandas as pd
import numpy as np
import os.path
import os
import shutil

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
    #        if "nose" in line.strip("\n"):
    #            f.write(line)
            if "swallow" in line.strip("\n"):
                f.write(line)

def slicing_audio(audio_track, name, number, seconds):
    '''
    This function creates audio slices of a specified length in milliseconds and stores these in a designated folder.
    Each slice has attached to its name the second it starts in the entire audio segment, e.g. slice 14 is the slice
    that starts at second 14 in the audio segment. The last slice, if shorter than the specified length, is omitted.
    '''

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = seconds * 1000

    # create a folder to store the slices in
    if os.path.isdir(f"audio_files/{name}/{name}_slices_{seconds}/") == False:
        os.mkdir(f"audio_files/{name}/{name}_slices_{seconds}/")
        os.mkdir(f"audio_files/{name}/{name}_slices_{seconds}/{name}_{number}/")
    else:
        os.mkdir(f"audio_files/{name}/{name}_slices_{seconds}/{name}_{number}/")

    for milsec in range(0, len(audio_track), milliseconds):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/{name}/{name}_slices_{seconds}/{name}_{number}/{name}_{number}_slice_{int(milsec/1000)}.mp3",
                format="mp3")

def create_stamp_list(path):
    '''
    This function creates a list of stamps that will be used in the subsequent step of the process of labelling the slices
    '''
    df = pd.read_csv(path, names=["start", "end", "label"], delimiter="\t")
    stamp_list = []
    for (stamp_start, stamp_end) in zip(df.loc[:, "start"],
                                    df.loc[:, "end"]):
        stamp_list.append(stamp_start)
        stamp_list.append(stamp_end)
    return stamp_list

def create_label_list(stamp_list, path_slices, seconds):
    '''
    This function loops over all seconds x at which a slice starts (0, 2, 4, ... ) and checks if
    any timestamp of the stamp list is included in the range x and x + 2 . If yes, the label is 1, else 0.
    First, we determine the number of slices by counting the files in the slices folder.
    Then, we loop of all starting seconds and check for a time stamp in that range.
    '''

    list_slices = os.listdir(path_slices)
    number_slices = len(list_slices)

    label_list = []
    for i in range(0, (number_slices * seconds), seconds):
        '''
        In each iteration i the test number is changed to something greater than 0 if there is at least one time stamp
        that falls in the range of i and i+2.
        '''
        test_number = 0
        for element in stamp_list:
            if element > i and element < (i + seconds):
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
            os.remove(f"audio_files/{name}/{name}_slices_{seconds}/{name}_{number}/{name}_{number}_slice_{i * seconds}.mp3")
            k += 1
            if k == n_to_delete:
                break
    return label_list

def extend_labels(label_list, seconds):
    '''
    This function adds the new labels to the list of all collected labels for training,
    or creates the list if not existent.
    '''

    if os.path.isfile(f"labels/labels_{seconds}.txt"):
        # load the collective labels into a list
        labels = np.loadtxt(f"labels/labels_{seconds}.txt", comments="#", delimiter="\n", unpack=False)
        list = [int(i) for i in labels]

        # concatenate with the new label list and save
        new_labels = list+label_list
        with open(f'labels/labels_{seconds}.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in new_labels)
    else:
        with open(f'labels/labels_{seconds}.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in label_list)

def load_spectrogram(path, list, seconds):
    '''
    This function creates a spectrogram of each slice, saves all of them in an numpy array
    and stores them in data.txt. It also deletes the audio slices for saving space.
    '''

    # convert each slice into a mel spectrogram and append it to a list
    for slice in os.listdir(path):
        if "mp3" in slice:
            audio, sr = librosa.load(path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            list.append(spectrogram_db)

    # convert the new collective data back to numpy array
    array = np.array(list)

    # save the array to a txt file
    file = open(f"data/data_{seconds}.txt", "w")
    for row in array:
        np.savetxt(file, row)

def extend_data(path, name, number, seconds):
    '''
    This function extends the collection of all data with the new slices,
    or creates the collection if not existent.
    '''

    # get the image size for reshaping the data file by picking out the first file in the slice folder
    k = 0
    for slice in os.listdir(path):
        if "mp3" in slice:
            audio, sr = librosa.load(path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            width = spectrogram_db.shape[1]
            k += 1
        if k > 0:
            break

    if os.path.isfile(f"data/data_{seconds}.txt"):
        # load collection of all data into an array
        data = np.loadtxt(f"data/data_{seconds}.txt")
        data = data.reshape(-1, 128, width)

        # create a copy that will be extended with new slices
        dim = data.shape[0]
        data_new = [data[i] for i in range(0, dim)]

        # load the slices into mel spectrograms and save it as an array
        load_spectrogram(path, data_new, seconds)

    else:
        data_list = []

        # load the slices into mel spectrograms and save it as an array
        load_spectrogram(path, data_list, seconds)

    # load the file that keeps track of the order of the data and append the new audio file name
    with open(f"data/order_of_data_{seconds}.txt", "a") as a_file:
        a_file.write("\n")
        a_file.write(f"{name}_{number}")

def test(seconds, path):
    '''
    This function prints the current shape of the data array and the distribution of 1's and 0's.
    It also shows the class distribution.
    '''
    # get the image size for reshaping the data file by picking out the first file in the slice folder
    k = 0
    for slice in os.listdir(path):
        if "mp3" in slice:
            audio, sr = librosa.load(path + slice)
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
            spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
            width = spectrogram_db.shape[1]
            k +=1
        if k > 0:
            break

    # loads and prints the shape of the data array
    data = np.loadtxt(f"data/data_{seconds}.txt")
    data = data.reshape(-1, 128, width)
    print(f"The current shape of your data is {data.shape}.")

    # loads the label list and counts the number of elements in each clasee
    labels = np.loadtxt(f"labels/labels_{seconds}.txt")
    print(f"class 0 has {list(labels).count(0)} elements.")
    print(f"class 1 has {list(labels).count(1)} elements.")

def add_new_data_and_labels(name, number, seconds):
    '''
    This function puts all the steps together for extending both the data and the labels with a new audio file
    '''

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files/{name}/{name}_{number}.mp3"
    path_labels = f"label_collections/{name}/{name}_{number}.txt"

    # loading the audio file from the specified path
    audio_file = AudioSegment.from_mp3(path_audio)

    # cleaning the label file of unwanted lines (that are created during the audio labelling process
    clean_labels(path_labels)

    # slicing the audio file and storing it in a designated folder
    slicing_audio(audio_file, name, number, seconds)

    # creating a variable for the created folder with the slices
    path_slices = f"audio_files/{name}/{name}_slices_{seconds}/{name}_{number}/"

    # create the stamp list
    stamp_list = create_stamp_list(path_labels)

    # creates the label list for the audio slices
    label_list = create_label_list(stamp_list, path_slices, seconds)

    # creates new balanced label list and deletes the corresponding slices
    new_label_list = delete_zeros(label_list, name, number, seconds)

    # append new label list to the list of all collected labels
    extend_labels(new_label_list, seconds)

    # extend the data with new slices
    extend_data(path_slices, name, number, seconds)

    # print the current shape of the data
    test(seconds, path_slices)

    # delete the audio slices
    location = f"/Users/albert/Desktop/Misophonia_Filter/audio_files/{name}"
    dir = f"{name}_slices_{seconds}"
    path = os.path.join(location, dir)
    shutil.rmtree(path, ignore_errors=False)


# specify in the arguments:
# (1) the name_surname,
# (2) number of audio file of that source and
# (3) the slice length in seconds
# example: "Steve_Brunton", 3, 2
add_new_data_and_labels("Recording", 7, 1)