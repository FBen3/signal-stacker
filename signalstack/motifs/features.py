# signalstack/motifs/features.py
import numpy as np


def rms(data_dict, *args):
    """Compute the root-mean-square (RMS) of each channel 
    in the signal.

    Parameters
    ----------
    data_dict : dict 
        Input data dict with keys 'data', 'fs', 'columns', 'meta'.
    *args 
        Unused, kept for pipeline signature compatibility.

    Returns
    -------
    dict
    """
    data = data_dict.get("data")
    # compute RMS along the time axis (axis=0)
    rms_vals = np.sqrt(np.mean(np.square(data), axis=0))
    # reshape to (1, C)
    rms_array = rms_vals.reshape(1, -1)

    # build output dict
    return {
        "data": rms_array,
        "fs": data_dict.get("fs"),
        "columns": data_dict.get("columns"),
        "meta": {**data_dict.get("meta", {}), "feature": "rms"}
    }


def mean(data_dict, *args):
    """Compute the mean value of each channel in the signal.

    Parameters
    ----------
    data_dict : dict
        Input data dict with keys 'data', 'fs', 'columns', 'meta'.
    *args
        Unused, kept for pipeline signature compatibility.

    Returns
    -------
    dict
        Data dict where 'data' is a 2D array of shape (1, C) containing mean values per channel.
    """
    data = data_dict.get("data")
    mean_vals = np.mean(data, axis=0)
    mean_array = mean_vals.reshape(1, -1)

    return {
        "data": mean_array,
        "fs": data_dict.get("fs"),
        "columns": data_dict.get("columns"),
        "meta": {**data_dict.get("meta", {}), "feature": "mean"}
    }


def pass_through(data_dict, *args):
    """
    Pass the data_dict through unchanged (stub or debug purpose).
    """
    return data_dict
