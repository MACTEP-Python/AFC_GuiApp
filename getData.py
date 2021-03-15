from scipy.io import wavfile


def getdata(filepath):
    sample, data = wavfile.read(filepath)
    return sample, data
