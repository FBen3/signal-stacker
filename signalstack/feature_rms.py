def rms(signal_dict, *args):
    data = signal_dict["data"]
    rms_val = np.sqrt(np.mean(data**2, axis=-1))
    signal_dict["meta"]["rms"] = rms_val
    print(f"[Feature] RMS extracted: {rms_val}")
    return signal_dict

# add a window  param for windowed RMS later.


# PLOTTING FUNCTION 
import matplotlib.pyplot as plt

def plot(signal_dict, *args):
    data = signal_dict["data"]
    plt.plot(data)
    plt.title("Filtered Signal")
    plt.xlabel("Time (samples)")
    plt.show()
    return signal_dict
