import os
from tqdm import tqdm
from pydub import AudioSegment

def slice_audio(name, number, seconds, overlap, class_no, cat):
    """
    This function takes in an audio file and slices it into pieces of specified length. These slices are
    then stored in a designated folder.
    The parameters help to save the data in a structured manner.
    """

    # specify the path to the audio file
    path_audio = f"audio_files/class_{class_no}/{cat}/{name}_{number}.mp3"

    # load the audio file from the specified path
    audio = AudioSegment.from_mp3(path_audio).set_frame_rate(22050)

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = int(seconds * 1000)

    # create a folder to store the slices in, in case it doesn't exist yet
    if os.path.isdir(f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}")

    # create slices of the audio file of length "seconds"
    for milsec in range(0, len(audio), milliseconds):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio):
            slice = audio[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}/{name}_{number}_slice_{milsec/1000}.mp3",
                format="mp3")


# loop over all audio files and apply the function
# apply function with the following parameters:
# name of the audio file,
# the slice length
# how much overlap between the slices
# which label class does it belong to
# which category does it belong to

for i in tqdm(range(1, 9)):
    slice_audio("speech_train", i, 0.2, 0, 0, "Train")

for i in tqdm(range(1, 4)):
    slice_audio("speech_test", i, 0.2, 0, 0, "Test")

for i in tqdm(range(1, 4)):
    slice_audio("speech_val", i, 0.2, 0, 0, "Validation")

for i in tqdm(range(1, 14)):
    slice_audio("ASMR_train", i, 0.2, 0, 1, "Train")

for i in tqdm(range(1, 4)):
    slice_audio("ASMR_test", i, 0.2, 0, 1, "Test")

for i in tqdm(range(1, 4)):
    slice_audio("ASMR_val", i, 0.2, 0, 1, "Validation")