import numpy as np
import matplotlib.pyplot as plt


def plot(data_dict, *args):
    """Plot the data in data_dict.

    - If data has multiple time samples (rows > 1), plots each channel over time.
    - If data has a single row (features), plots a bar chart of channel values.

    Parameters
    ----------
    data_dict : dict
        Input dict with keys 'data', 'fs', 'columns', 'meta'.
    *args
        Unused, kept for pipeline signature compatibility.

    Returns
    -------
    dict
    """
    data = data_dict.get("data")  # shape: (N, C)
    columns = data_dict.get("columns", [])
    fs = data_dict.get("fs", None)

    # determine if time-series or single-row features
    n_samples, n_channels = data.shape

    plt.figure()
    if n_samples > 1:
        # time axis: sample index or time in seconds if fs is known
        if fs:
            t = np.arange(n_samples) / fs
            plt.xlabel('Time (s)')
        else:
            t = np.arange(n_samples)
            plt.xlabel('Sample index')

        for ch in range(n_channels):
            plt.plot(t, data[:, ch], label=columns[ch] if columns else None)
        if columns:
            plt.legend(loc='best')
        plt.title('Time-series Plot')
        plt.tight_layout()
    else:
        # bar chart for single-row features
        values = data.flatten()
        indices = np.arange(n_channels)
        plt.bar(indices, values)
        if columns:
            plt.xticks(indices, columns, rotation=45, ha='right')
        plt.ylabel('Value')
        plt.title('Feature Values')
        plt.tight_layout()

    plt.show()

    return data_dict
