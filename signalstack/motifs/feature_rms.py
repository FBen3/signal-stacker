import numpy as np

# ---- MEAN ----
def mean(signal_dict, *args):
    data = signal_dict["data"]
    if data.shape[0] > data.shape[1]:
        data = data.T
    mean_val = np.mean(data, axis= 1)  # One mean per channel
    signal_dict.setdefault("features", {})["mean"] = mean_val
    print(f"[Feature] Mean: {mean_val}")
    return signal_dict

# ---- RMS ----
def rms(signal_dict, *args):
    data = signal_dict["data"]
    print("Data shape:", data.shape)
    if data.shape[0] > data.shape[1]:
        data = data.T
    rms_val = np.sqrt(np.mean(np.square(data), axis=1))  # One RMS per channel
    signal_dict.setdefault("features", {})["rms"] = rms_val
    print(f"[Feature] RMS: {rms_val}")
    return signal_dict

def fftpeak(signal_dict, *args):
    data = signal_dict["data"]
    fs = signal_dict.get("fs")
    if fs is None:
        raise ValueError("Sampling rate 'fs' must be specified in signal_dict.")

    # Transpose if shape is (samples, channels)
    if data.shape[0] > data.shape[1]:
        data = data.T  # shape: (channels, samples)

    if data.shape[0] == 33:  # already (channels, samples)
        pass
    elif data.shape[1] == 33:  # probably (samples, channels)
        data = data.T  # transpose to (channels, samples)
    else:
        raise ValueError("Unexpected data shape")

    data = data - np.mean(data, axis=1, keepdims=True)

    N = data.shape[1]  # number of samples
    freqs = np.fft.rfftfreq(N, d=1/fs)

    peak_freq = []
    for channel in data:
        power = np.abs(np.fft.rfft(channel))**2
        peak = freqs[np.argmax(power)]
        peak_freq.append(peak)

    peak_freq = np.array(peak_freq)
    signal_dict.setdefault("features", {})["fft_peak"] = peak_freq
    print(f"[Feature] FFT Peak Frequency: {peak_freq}")
    return signal_dict


