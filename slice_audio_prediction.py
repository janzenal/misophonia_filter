from pydub import AudioSegment
import os

def slice_audio(name, number, seconds, overlap):
    """
    This function slices an audio file for prediction and saves the slices in a designated folder.
    """

    # loading the audio file and the corresponding label file
    path_audio = f"audio_files/for_prediction/{name}/{name}_{number}.mp3"

    # loading the audio file from the specified path
    audio_track = AudioSegment.from_mp3(path_audio).set_frame_rate(22050)

    # since the length of the audio file is stored in milliseconds, we have to convert our input to milliseconds
    milliseconds = int(seconds * 1000)

    # create a folder to store the slices in, in case it doesn't exist yet
    if os.path.isdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}") == False:
        os.mkdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}")
    if os.path.isdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}") == False:
        os.mkdir(f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/{name}_{number}")

    for milsec in range(0, len(audio_track), milliseconds):
        slice_start = milsec
        slice_end = slice_start + milliseconds
        if slice_end < len(audio_track):
            slice = audio_track[slice_start: slice_end]
            slice.export(
                out_f=f"audio_files/for_prediction/{name}/seconds_{seconds}_overlap_{overlap}/"+
                      f"{name}_{number}/{name}_{number}_slice_{milsec/1000}.mp3",
                format="mp3")

# apply function with the following parameters:
# name of the audio file
# which number of that audio file
# the slice length
# how much overlap between the slices
slice_audio("Recording", 1, 0.2, 0)

