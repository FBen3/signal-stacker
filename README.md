> A modular, chainable neuro/biosignal pipeline system where each stage (called a motif) processes time series data: filtering, feature extraction, classification, plotting, etc.

**Problem**:

Most scientists working with EMG/EEG/etc. have to:
- write a new script every time they want to process data
- copy-paste code for filtering, FFTs, visualizations, etc.
- struggle to reproduce or modify old analyses.

What if you could just define a sequence of named blocks like: `raw_data → bandpass_filter → RMS_feature → kNN_classifier → plot`

**Example usage**:

`signalstack --pipeline "load:mock.csv | features:rms | classify:knn:1 | outputs:plot" --verbose`

**Project structure**:

```
signalstack/
├── motifs/
│   ├── classify.py
│   ├── features.py
│   ├── filters.py
│   ├── load.py
│   ├── models.py
│   └── outputs.py
├── core/
│   └── pipeline.py      # Chain logic: input → motifs → output
├── data/
│   └── mock_eeg.csv
├── main.py              # Entrypoint
├── uv.lock
└── pyproject.toml
```
