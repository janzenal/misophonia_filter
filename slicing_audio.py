from pydub import AudioSegment
import os

def slicing_audio(audio_track, name, number, seconds, overlap, class_no):

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = seconds * 1000

    # create a folder to store the slices in, in case it doesn't exist yet
    if os.path.isdir(f"audio_files/class_{class_no}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"audio_files/class_{class_no}/seconds_{seconds}_overlap_{overlap}")

    for milsec in range(0, len(audio_track), milliseconds):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/class_{class_no}/seconds_{seconds}_overlap_{overlap}/{name}_{number}_slice_{int(milsec/1000)}.mp3",
                format="mp3")

def perform_on_class(name, number, seconds, overlap, class_no):

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files/class_{class_no}/{name}_{number}.mp3"

    # loading the audio file from the specified path
    audio_file = AudioSegment.from_mp3(path_audio)

    # slicing the audio file and storing it in a designated folder
    slicing_audio(audio_file, name, number, seconds, overlap, class_no)

#perform_on_class("ASMR", 14, 1, 0, 1)