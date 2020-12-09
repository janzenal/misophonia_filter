from pydub import AudioSegment
import os
import librosa
import numpy as np

def slicing_audio(name, number, seconds, overlap):

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files/for_prediction/{name}/{name}_{number}.mp3"

    # loading the audio file from the specified path
    audio_track = AudioSegment.from_mp3(path_audio)

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = int(seconds * 1000)

    # create a folder to store the slices in, in case it doesn't exist yet
    if os.path.isdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}")
    if os.path.isdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}") == False:
        os.mkdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}")

    for milsec in range(0, len(audio_track), int(milliseconds*0.5)):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/"+
                      f"{name}_{number}/{name}_{number}_slice_{milsec/1000}.mp3",
                format="mp3")

def create_data(name, number, seconds, overlap):
    '''
    This function creates a spectrogram of each slice and saves the result as a numpy array in data.txt.
    '''

    path_slices = f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}/"

    # collect all the slices in a list
    data_list = []

    for slice in os.listdir(path_slices):
        if "mp3" in slice:
                wav_path = slice.replace("mp3", "wav")

            # convert wav to mp3
                sound = AudioSegment.from_mp3(path_slices + slice)
                sound = sound.set_frame_rate(16000)
                sound.export(path_slices + "wav_compressed/" + wav_path, format="wav")
                wav_file, sr = librosa.load(path_slices + "wav_compressed/" + wav_path)
                data_list.append(wav_file)

    # convert the list to a numpy array
    array = np.array(data_list)

    # save the array to a txt file
    if os.path.isdir(f"data_wav_compressed/for_prediction/{name}") == False:
        os.mkdir(f"data/for_prediction/{name}")
    if os.path.isdir(f"data_wav_compressed/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"data_wav_compressed/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}")
    if os.path.isdir(f"data_wav_compressed/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}") == False:
        os.mkdir(f"data/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}")
    file = open(f"data/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}/data.txt", "w")
    for row in array:
        np.savetxt(file, row)

slicing_audio("Recording", 1, 0.2, 0)

create_data("Recording", 1, 0.2, 0)
