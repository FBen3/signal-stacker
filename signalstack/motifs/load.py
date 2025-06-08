# Convert all file types into main filetype ( CSV ) -n single internal format 
# The reason why we chose CSV is because it is a very flexible file format that can be used and esy to process. 
# This approach simpfiles worklow, keeps the motifs consistent 

# note: we can either convert these different file types to CSV or standardised numpy array 

import pandas as pd 
import mne  
import scipy.io 
import numpy as np 
import os 
import pyxdf


# # ensure that they all retrun numpy array 
# # bETTER to convert to numpy array rather than CSV format as it is more efficient and easier to process, cleaner code 
# def load_data(filepath):
#     ext = os.path.splitext(filepath)[1].lower()
#     if ext == '.csv':
#         df = pd.read_csv(filepath)
#         return df.values  # convert to ndarray
#     elif ext == '.edf':
#         raw = mne.io.read_raw_edf(filepath, preload=True)
#         return raw.get_data()  # returns ndarray
#     elif ext == '.mat':
#         mat = scipy.io.loadmat(filepath)
#         return mat['data']  # ensure it's ndarray
#     elif ext == '.npy':
#         return np.load(filepath)
#     elif ext == 'tsv':
#         tsv = pd.read_csv(filepath, sep='\t')
#         return tsv.values 
#     elif ext == 'xdf': 
#         xdf = pyxdf.load_xdf(filepath)
#         return xdf[0]
#     elif ext == 'fif':
#         fif = mne.io.read_raw_fif(filepath, preload=True)
#         return fif.get_data()
#     else:
#         raise ValueError(f\"Unsupported file format: {ext}\")








#  Recommended format:
# Use a Python dict like this:

# {
#   "data": np.ndarray,         # shape: (N, C) or (N,) — time x channels
#   "fs": float,                # sampling rate, if known
#   "columns": List[str],       # column names, if available
#   "meta": Dict[str, Any],     # optional metadata
# }

# use dictionary to store the data but consider all file types which are now converted to numpy array 

# data: np.ndarray- 	Core signal data, standard shape (samples × channels or samples only)
# fs: float- 	Essential for filters, FFTs, time-based windows
# columns: List[str]- 	Useful for labeled channels (EEG/EMG electrodes)
# meta: Dict[str, Any]-  Flexible: can store subject ID, source file name, experiment info, labels, etc.

def signal_dict(data, fs=None, columns=None, meta=None):
    return {
        "data": data,
        "fs": fs if fs is not None else 1000.0,  # default
        "columns": columns,
        "meta": meta or {}
    }


# redefining the load function - muuch better as it incorporates the signal_dict function in a much cleaner way 

def load(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    meta = {"source_file": filepath}
    
    if ext == '.csv':
        df = pd.read_csv(filepath)
        return signal_dict(df.values, columns=list(df.columns), meta=meta)
    
    elif ext == '.npy':
        data = np.load(filepath)
        return signal_dict(data, meta=meta)  # this is a placeholder 
    
    elif ext == '.mat':
        mat = scipy.io.loadmat(filepath)
        data = mat.get("data") or mat[list(mat.keys())[-1]]
        fs = mat.get("fs", 1000)
        return signal_dict(data, fs=fs, meta=meta)
    
    elif ext == '.edf':
        raw = mne.io.read_raw_edf(filepath, preload=True)
        data = raw.get_data().T
        fs = raw.info['sfreq']
        columns = raw.ch_names
        return signal_dict(data, fs=fs, columns=columns, meta=meta)
    
    elif ext == 'tsv':
        df = pd.read_csv(filepath, sep='\t')
        return signal_dict(df.values, columns=list(df.columns), meta=meta)
    
    elif ext == 'xdf':
        xdf = pyxdf.load_xdf(filepath)
        return signal_dict(xdf[0], meta=meta)  # This is a placeholder 
    
    elif ext == 'fif':
        fif = mne.io.read_raw_fif(filepath, preload=True)
        data = fif.get_data()
        fs = fif.info['sfreq']
        columns = fif.ch_names
        return signal_dict(data, fs=fs, columns=columns, meta=meta)
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# def bandpass_filter(signal_dict, )

# def bandpass_filter(signal_dict, low_freq, high_freq):
#     data= signal_dict["data"]
#     fs= signal_dict["fs"]
    
#     ...

#     return 



