import librosa 
def getSpectro(song, M):
    #Get a sprectrogram out of a mp3
    audioData, sr = librosa.load(song) 
    audioData = librosa.util.normalize(audioData)
    stft = np.abs(librosa.core.stft(audioData)) ** 2 #Make spectro once so we don't have to recompute it

    #Mel spectrogram 
    melSpec = librosa.feature.melspectrogram(S = stft)
    mfcc    = librosa.feature.mfcc(S = stft)
    chroma  = librosa.feature.chroma_stft(S = stft)

    #Grab a random start idx to slice the array
    #TODO: Figure out a way to get a M length feature by cutting audioData directly
    idxSection = int(np.random.uniform(0, melSpec.shape[1] - M))

    melSpec = melSpec[:, idxSection:idxSection + M]
    mfcc    = mfcc[:, idxSection:idxSection + M]
    chroma  = chroma[:, idxSection:idxSection + M]

    melSpec = np.log(melSpec + 1e-9)
        
    melSpec = librosa.util.normalize(melSpec)
    mfcc    = librosa.util.normalize(mfcc)
    chroma  = librosa.util.normalize(chroma)

    #Pad to fit the shape of melSpec
    mfcc    = np.pad(mfcc, pad_width=((0, 108), (0, 0)))
    chroma  = np.pad(chroma, pad_width=((0, 116), (0, 0)))[:, :M]
    
    #add axis to concatenate
    chroma  = np.expand_dims(chroma, axis = 0)

    #Stack it up into a 3D Matrix
    S = np.stack((melSpec, mfcc))
    S = np.concatenate((S, chroma))
    S = np.swapaxes(S, 0, 2)

