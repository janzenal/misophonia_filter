from tqdm import tqdm
import numpy as np
import os.path
import os
from pydub import AudioSegment


def create_data(name, number, seconds, overlap):

    path_slices = f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}/"

    data_list = []

    # load each slice into a numpy array
    for i, slice in tqdm(enumerate(os.listdir(path_slices))):
        if "mp3" in slice:

            audio = AudioSegment.from_mp3(path_slices + slice)

            if audio.channels == 2:
                audio = audio.set_channels(1)

            array = np.array(audio.get_array_of_samples())
            if array.shape[0] < 9600:
                pad = np.zeros((9600 - array.shape[0],))
                array = np.concatenate((array, pad), axis=0)
            data_list.append(array)

            # convert the list to a numpy array
            array = np.array(data_list)

            if os.path.isdir(f"data_mp3/for_prediction/{name}") == False:
                os.mkdir(f"data_mp3/for_prediction/{name}")
            if os.path.isdir(f"data_mp3/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}") == False:
                os.mkdir(f"data_mp3/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}")
            if os.path.isdir(f"data_mp3/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}") == False:
                os.mkdir(f"data_mp3/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}")
            np.save(f"data_mp3/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}/data_mp3.npy", array)
            data_list = []

create_data("Olaf_Schubert", 1, 0.2, 0)