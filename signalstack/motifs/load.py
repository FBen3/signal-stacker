import numpy as np
import pandas as pd


def load_csv(input_dict, path, fs=None):
    """Load time-series data from a CSV file 
    into the pipeline format.

    Args:
        input_dict (dict or None): Ignored, present for consistency in pipeline.
        path (str): Path to the CSV file to load.
        fs (str or float, optional): Sampling rate. If provided as string, it will be converted to float. Defaults to 1000.0.

    Returns:
        dict: A standardized data dict with keys: 'data', 'fs', 'columns', 'meta'.
    """
    # Read CSV into DataFrame
    df = pd.read_csv(path)

    # Convert DataFrame to numpy array
    arr = df.values
    # Ensure 2D shape: (N, C)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)

    # Determine sampling rate
    try:
        sample_rate = float(fs) if fs is not None else 1000.0
    except ValueError:
        raise ValueError(f"Invalid sampling rate: {fs}")

    # Build standardized output dict
    return {
        "data": arr,
        "fs": sample_rate,
        "columns": df.columns.tolist(),
        "meta": {
            "source": path,
            "num_samples": arr.shape[0],
            "num_channels": arr.shape[1]
        }
    }
