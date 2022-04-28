import librosa 
import numpy as np
import scipy.io.wavfile
import torch

from .music_analyzer import MusicAnalyzer

class EmbedderAnalyzer():
    _FEATURE_NAME = "embedding"
    def __init__(
            self,
            model,
            fft_length):
        super().__init__()
        model = model
        fft_length = fft_length

    def _preprocess(self, song):
        #Get a sprectrogram out of a mp3
        audio_data, _ = librosa.load(song, sr=None) 
        audio_data = librosa.util.normalize(audio_data)
        stft = np.abs(librosa.core.stft(audio_data)) ** 2 

        #Mel spectrogram 
        mel_spec = librosa.feature.melspectrogram(S = stft)
        mfcc    = librosa.feature.mfcc(S = stft)
        chroma  = librosa.feature.chroma_stft(S = stft)

        #Grab a random start idx to slice the array
        #TODO: Figure out a way to get a M length feature by cutting audioData directly
        idx_section = int(np.random.uniform(0, mel_spec.shape[1] - self.fft_length))

        mel_spec = mel_spec[:, idx_section:idx_section + self.fft_length]
        mfcc    = mfcc[:, idx_section:idx_section + self.fft_length]
        chroma  = chroma[:, idx_section:idx_section + self.fft_length]

        mel_spec = np.log(mel_spec + 1e-9)
            
        mel_spec = librosa.util.normalize(mel_spec)
        mfcc     = librosa.util.normalize(mfcc)
        chroma   = librosa.util.normalize(chroma)

        #Pad to fit the shape of melSpec
        mfcc    = np.pad(mfcc, pad_width=((0, 108), (0, 0)))
        chroma  = np.pad(chroma, pad_width=((0, 116), (0, 0)))[:, :self.fft_length]
        
        #add axis to concatenate
        chroma  = np.expand_dims(chroma, axis = 0)

        #Stack it up into a 3D Matrix
        S = np.stack((mel_spec, mfcc))
        S = np.concatenate((S, chroma))
        S = np.swapaxes(S, 0, 2)

        S = np.expand_dims(S, axis = 0)

        return S
    
    def _analyze(self, S):
        return self.model.predict(S).flatten()

    @classmethod
    def from_config(cls,
            config):
        model = torch.nn.Module()
        model.load_state_dict(config['embedder']['path'])
        model.eval()

        fft_length = config['embedder']['fft_length']

        return cls(model = model,
                fft_length = fft_length)
