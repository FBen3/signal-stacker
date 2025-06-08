import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


def knn(parcel: dict,
        *args,                       # ← NEW: positional CLI args
        n_neighbors: int = 3,        # still usable as keyword
        label_column: str | None = None):
    """
    Fit a quick K-Nearest-Neighbours model and append a ``predicted_label`` column.

    * If the pipeline string supplies an extra positional token
      (e.g. ``classify:knn:1``) it is treated as ``n_neighbors``.
    * Works whether ``parcel["data"]`` is a NumPy array **or** a DataFrame.
    * Always converts the data back to a NumPy array so downstream motifs,
      like ``outputs.plot``, still receive what they expect.
    """

    # ── handle CLI override ────────────────────────────────────────────────────────
    if args:                                 # first extra arg → k
        try:
            n_neighbors = int(args[0])
        except ValueError:
            raise ValueError("First positional arg to knn must be an integer (k)")

    if not isinstance(parcel, dict) or "data" not in parcel:
        raise TypeError("Expecting the running-parcel dict with a 'data' key")

    raw = parcel["data"]
    columns = parcel.get("columns", []) or []

    # ── ensure we are working with a DataFrame ─────────────────────────────────────
    if isinstance(raw, np.ndarray):
        if not columns:
            columns = [f"ch{i}" for i in range(raw.shape[1])]
        df = pd.DataFrame(raw, columns=columns)
    elif isinstance(raw, pd.DataFrame):
        df = raw.copy()
    else:
        raise TypeError(f"'data' must be ndarray or DataFrame, not {type(raw)}")

    # ── decide on an effective k that will not explode with few samples ───────────
    k_eff = max(1, min(n_neighbors, len(df)))          # clamp to sample count
    if k_eff != n_neighbors:
        print(f"[knn] Only {len(df)} sample(s); clamping k to {k_eff}")

    # ── prepare X / y ──────────────────────────────────────────────────────────────
    if label_column and label_column in df.columns:
        X = df.drop(columns=[label_column]).to_numpy()
        y = df[label_column].to_numpy()
    else:
        X = df.to_numpy()
        y = np.arange(len(df))                         # dummy labels for the demo

    # ── train & predict ────────────────────────────────────────────────────────────
    model = KNeighborsClassifier(n_neighbors=k_eff)
    model.fit(X, y)
    df["predicted_label"] = model.predict(X)

    # ── hand parcel back in NumPy form so later motifs remain happy ───────────────
    parcel["data"] = df.to_numpy()
    parcel["columns"] = df.columns.tolist()
    return parcel
