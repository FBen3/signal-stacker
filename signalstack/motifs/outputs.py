import numpy as np
import matplotlib.pyplot as plt


def _axis_labels(meta: dict) -> tuple[str, str, str]:
    """Decide x-label, y-label and title based on the 
    feature that produced the current single-row table 
    (e.g. 'rms', 'mean').  Returns a triple: (xlabel, ylabel, title)
    """
    feature = meta.get("feature", "").lower()
    xlabel  = "Channel index"

    if feature == "rms":
        return xlabel, "RMS amplitude", "RMS Features"
    if feature == "mean":
        return xlabel, "Mean amplitude", "Mean Features"

    # fall-back for any other feature type
    return xlabel, "Value", "Feature Values"


def plot(data_dict, *args):
    """If the parcel contains a single row AND a 'predicted_label' column,
    draw a 1×2 figure:
          ┌───────────────┬───────────────┐
          │ feature bars  │  big label    │
          └───────────────┴───────────────┘
      The left panel’s axes are chosen according to the feature motif
      that ran last ('rms' → “RMS amplitude”, etc.).

    Otherwise fall back to the older behaviour, but still label the axes
    intelligently when the data are single-row features.
    """
    data       = data_dict.get("data")
    columns    = data_dict.get("columns", [])
    fs         = data_dict.get("fs")
    meta       = data_dict.get("meta", {})

    n_samples, n_channels = data.shape
    single_row  = n_samples == 1
    has_predcol = "predicted_label" in columns

    if single_row and has_predcol:
        pred_idx   = columns.index("predicted_label")
        pred_value = float(data[0, pred_idx])

        xlabel, ylabel, title = _axis_labels(meta)

        fig, (ax_feat, ax_label) = plt.subplots(
            1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [3, 1]}
        )

        feat_mask = np.arange(n_channels) != pred_idx
        ax_feat.bar(np.arange(n_channels)[feat_mask], data[0, feat_mask])

        # numeric channel ticks so “Unnamed: 0” headers disappear
        ax_feat.set_xticks(np.arange(n_channels)[feat_mask])
        ax_feat.set_xticklabels(np.arange(n_channels)[feat_mask], rotation=45, ha="right")

        ax_feat.set_xlabel(xlabel)
        ax_feat.set_ylabel(ylabel)
        ax_feat.set_title(title)

        # right panel: big predicted label
        ax_label.axis("off")
        ax_label.text(
            0.5, 0.5,
            f"Predicted\nlabel\n{int(pred_value)}",
            fontsize=24, fontweight="bold",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.5", fc="#ffdddd", ec="#aa0000", lw=2)
        )

        fig.tight_layout()
        plt.show()
        return data_dict

    plt.figure()

    # multi-sample (time-series) data
    if n_samples > 1:
        t = np.arange(n_samples) / fs if fs else np.arange(n_samples)
        plt.xlabel("Time (s)" if fs else "Sample index")
        for ch in range(n_channels):
            plt.plot(t, data[:, ch], label=columns[ch] if columns else None)
        if columns:
            plt.legend(loc="best")
        plt.title("Time-series Plot")
        plt.tight_layout()
        plt.show()
        return data_dict

    # single-row feature table (no classifier)
    xlabel, ylabel, title = _axis_labels(meta)
    indices = np.arange(n_channels)
    plt.bar(indices, data.flatten())

    # numeric ticks: 0 … N-1
    plt.xticks(indices, indices, rotation=45, ha="right")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    return data_dict
