import pydub
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

def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

audio = read("audio_files/for_prediction/Olaf_Schubert/seconds_0.2_overlap_0/Olaf_Schubert_1/Olaf_Schubert_1_slice_0.0.mp3")

aud, sr = librosa.load("audio_files/class_0/Train/seconds_0.2_overlap_0.1/wav/speech_train_8_slice_1.0.wav")
print(aud.shape)