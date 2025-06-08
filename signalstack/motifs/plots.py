import matplotlib.pyplot as plt
import numpy as np

def plot(signal_dict, *args):
    mode = args[0] if args else "signal"
    data = signal_dict.get("data")
    features = signal_dict.get("features", {})

    
    if mode == "signal":
    

        if data.ndim != 2:
            raise ValueError("Expected multichannel data with shape (channels, samples)")

        n_channels = data.shape[0]

        if n_channels >= 32:
            # Heatmap for 32+ channels
            plt.imshow(data.T, aspect='auto', cmap='viridis', interpolation='nearest')
            plt.colorbar(label="Amplitude")
            plt.xlabel("Time (samples)")
            plt.ylabel("Channels")
            plt.title("Multichannel Signal (Heatmap)")
            plt.tight_layout()
            plt.show()
        else:
            # Fallback: overlay every 4th channel
            plt.figure(figsize=(12, 5))
            for i, channel in enumerate(data):
                if i % 4 == 0:
                    plt.plot(channel, alpha=0.4, label=f"Ch {i+1}")
            plt.title("Multichannel Signal (Overlay)")
            plt.xlabel("Time (samples)")
            plt.ylabel("Amplitude")
            plt.legend(fontsize="small", ncol=3)
            plt.tight_layout()
            plt.grid(alpha=0.2)
            plt.show()

        return signal_dict


    # add the  plit for features as well 
    elif mode == "features":
        if not features:
            raise ValueError("No features found in signal_dict.")

        num_features = len(features)
        fig, axs = plt.subplots(num_features, 1, figsize=(12, 3 * num_features))

        if num_features == 1:
            axs = [axs]  # Make iterable

        for ax, (name, val) in zip(axs, features.items()):
            val = np.array(val)
            if val.ndim == 1:
                ax.bar(np.arange(len(val)), val)
                ax.set_xlabel("Channel")
                ax.set_ylabel("Value")
            else:
                ax.text(0.5, 0.5, f"Non-1D feature: {name}", ha="center", va="center")
            ax.set_title(name)

        fig.suptitle("Extracted Features", fontsize=16)
        plt.tight_layout()
        plt.show()
        return signal_dict

    
    else:
        raise ValueError(f"Unknown plot mode: '{mode}'. Use 'signal' or 'features'.")




    return signal_dict


