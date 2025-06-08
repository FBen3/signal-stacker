# Don’t hardcode 20–450. Let users pass the range, or infer a sensible default
# from context (meta, signal type, etc.). Support highpass, lowpass, and bandpass modes in the same function.



from scipy.signal import butter, filtfilt


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
    filtered = filtfilt(b, a, data, axis=0)
    signal_dict["data"] = filtered
    signal_dict["meta"]["filtered"] = filter_desc

    return signal_dict







# def bandpass_filter(signal_dict, low_freq, high_freq):
    
    # data= signal_dict["data"]
    # fs= signal_dict["fs"]

    # # check if the data is a numpy array 
    # if not isinstance(data, np.ndarray):
    #     raise ValueError("Data must be a numpy array")
    
    # # check if the low and high frequencies are valid 
    # if low_freq < 0 or high_freq > fs/2:
    #     raise ValueError("Invalid frequency range")
    
    # # create the filter 
    # nyquist_freq = 0.5 * fs 
    # low = low_freq / nyquist_freq 
    # high = high_freq / nyquist_freq 

    # # apply the filter 
    # filtered_data = butter_bandpass_filter(data, low, high, fs) 
    
    
