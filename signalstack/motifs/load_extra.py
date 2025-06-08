# for the .xdf files- repace this later with the place holder one 

# elif ext == '.xdf':
#     streams, _ = pyxdf.load_xdf(filepath)

#     eeg_stream = next((s for s in streams if s['info']['type'][0].lower() == 'eeg'), streams[0])

#     data = np.array(eeg_stream['time_series'])
#     fs = float(eeg_stream['info']['nominal_srate'][0])
#     timestamps = np.array(eeg_stream['time_stamps'])

#     try:
#         channel_info = eeg_stream['info']['desc'][0]['channels'][0]['channel']
#         columns = [ch['label'][0] for ch in channel_info]
#     except Exception:
#         columns = [f"Ch{i+1}" for i in range(data.shape[1])]

#     meta.update({
#         "stream_name": eeg_stream['info']['name'][0],
#         "manufacturer": eeg_stream['info']['manufacturer'][0],
#         "timestamps": timestamps.tolist(),
#         "original_format": "xdf"
#     })

#     return build_signal_dict(data, fs=fs, columns=columns, meta=meta)


# also for the .npy files use this:

# elif ext == '.npy':
#     data = np.load(filepath)
#     fs = 1000.0  # default, or accept as user argument in future
#     columns = [f"Ch{i+1}" for i in range(data.shape[1])] if data.ndim == 2 else None

#     meta.update({
#         "source_file": filepath,
#         "original_format": "npy"
#     })

#     return build_signal_dict(data, fs=fs, columns=columns, meta=meta)
