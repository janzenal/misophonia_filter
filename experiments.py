import pydub
from pydub import AudioSegment
import numpy as np
import librosa


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y


sound = AudioSegment.from_mp3("audio_files/class_0/Test/seconds_0.2_shuffled/wav_compressed/speech_test_1_slice_0.2.wav")
sound = sound.set_frame_rate(16000)
sound.export("speech_test_1_slice_0.2.wav", format="wav")
wav_file, sr = librosa.load("speech_test_1_slice_0.2.wav")
print(wav_file.shape)

