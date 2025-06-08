# Don’t hardcode 20–450. Let users pass the range, or infer a sensible default
# from context (meta, signal type, etc.). Support highpass, lowpass, and bandpass modes in the same function.



from scipy.signal import butter, filtfilt
from signalstack.motifs.load import signal
from signalstack.motifs.plots import plot
from signalstack.motifs.feature_rms import rms, mean, fftpeak


# Defaults:
#   if no freqs are specified, it looks at the device type in metadata - common freq ranges fot these types of signals:
#       for EMG: defaults to 20-450 HZ 
#       for EEG: defaults to 0.5-50 Hz

# Filter Creation:
#   creates 3 types of filters:
#       1- Bandpass (if both low and high are specified)
#       2- Highpass (if only low is specified)
#       3- Lowpass (if only high is specified)

# Filter Application:
#   applies the filter to the data using scipy.signal.filtfilt

# IMPORTNAT: 
#  the filter is applied along the first axis of the data (typically time)
# SHOULD consider applying along other axes as well. (2D, 3D, etc.)


def bandpass(signal_dict, *args):
    """
    Apply a bandpass, highpass, or lowpass filter depending on args.
    Args should be passed like: 'low=20', 'high=450'
    """
    fs = signal_dict.get("fs")
    data = signal_dict.get("data")
    meta = signal_dict.get("meta", {})
    
    if fs is None or data is None:
        raise ValueError("Signal must include 'data' and 'fs'.")

    # Parse arguments --
    arg_dict = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=')
            arg_dict[key.strip()] = float(value.strip())

    low = arg_dict.get("low")
    high = arg_dict.get("high")
    order = int(arg_dict.get("order", 4))

    # --- Smart default fallback ---
    if low is None and high is None:
        device = meta.get("recording_device", "").lower()
        if "emg" in device:
            low, high = 20.0, 450.0
        elif "eeg" in device:
            low, high = 0.5, 50.0
        else:
            raise ValueError("No cutoff frequencies specified and no known device info to infer defaults.")

    # --- Build filter ---
    nyq = fs / 2.0
    if low and high:
        b, a = butter(order, [low/nyq, high/nyq], btype='band')
        filter_desc = f"Bandpass: {low}-{high} Hz"
    elif low:
        b, a = butter(order, low/nyq, btype='high')
        filter_desc = f"Highpass: >{low} Hz"
    elif high:
        b, a = butter(order, high/nyq, btype='low')
        filter_desc = f"Lowpass: <{high} Hz"
    else:
        raise ValueError("Invalid filter setup.")

    # --- Apply filter ---
    filtered = filtfilt(b, a, data, axis=1) # changed axis from 0 to 1 for 2D data (multichannel)
    # can add addtional argguments here maybe later 
    signal_dict["data"] = filtered
    signal_dict["meta"]["filtered"] = filter_desc

    return signal_dict


# apply the bandpass filter to our file
if __name__ == "__main__":
    b_pass = bandpass(signal, "low= 0.5", "high= 50")
    plot(b_pass, "signal")

    # Ask user which feature to extract
    print("Which feature do you want to extract? (rms, mean, fftpeak, all)")
    feature = input("Enter your choice: ").strip().lower()

    b_pass["features"] = {}
    if feature == "rms":
        b_pass = rms(b_pass)
        print("RMS:", b_pass["features"]["rms"])
    elif feature == "mean":
        b_pass = mean(b_pass)
        print("Mean:", b_pass["features"]["mean"])
    elif feature == "fftpeak":
        b_pass = fftpeak(b_pass)
        print("FFT Peak:", b_pass["features"]["fft_peak"])
    elif feature == "all":
        b_pass = rms(b_pass)
        b_pass = mean(b_pass)
        b_pass = fftpeak(b_pass)
        print("RMS:", b_pass["features"]["rms"])
        print("Mean:", b_pass["features"]["mean"])
        print("FFT Peak:", b_pass["features"]["fft_peak"])
    else:
        print("Unknown feature. Please choose from: rms, mean, fftpeak, all.")

    # Optionally plot features if any were extracted
    if feature in ("rms", "mean", "fftpeak", "all"):
        plot(b_pass, "features")







