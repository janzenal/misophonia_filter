from pydub import AudioSegment
import os

def slicing_audio(audio_track, name, number, seconds, overlap, class_no, cat):

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = int(seconds * 1000)

    # create a folder to store the slices in, in case it doesn't exist yet
    if os.path.isdir(f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}")

    for milsec in range(0, len(audio_track), int(milliseconds*0.5)):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/class_{class_no}/{cat}/seconds_{seconds}_overlap_{overlap}/{name}_{number}_slice_{milsec/1000}.mp3",
                format="mp3")

def parameters(name, number, seconds, overlap, class_no, cat):

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files/class_{class_no}/{cat}/{name}_{number}.mp3"

    # loading the audio file from the specified path
    audio_file = AudioSegment.from_mp3(path_audio)

    # slicing the audio file and storing it in a designated folder
    slicing_audio(audio_file, name, number, seconds, overlap, class_no, cat)

def perform(seconds, overlap):
    for i in range(1, 9):
        parameters("speech_train", i, seconds, overlap, 0, "Train")

    for i in range(1, 4):
        parameters("speech_test", i, seconds, overlap, 0, "Test")

    for i in range(1, 4):
        parameters("speech_val", i, seconds, overlap, 0, "Validation")

    for i in range(1, 14):
        parameters("ASMR_train", i, seconds, overlap, 1, "Train")

    for i in range(1, 4):
        parameters("ASMR_test", i, seconds, overlap, 1, "Test")

    for i in range(1, 4):
        parameters("ASMR_val", i, seconds, overlap, 1, "Validation")

perform(1.5, 0.5)