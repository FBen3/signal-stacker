import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

def knn(parcel: dict, *, n_neighbors: int = 3, label_column: str | None = None):
    """
    Append a ``predicted_label`` column to the parcel’s DataFrame using
    a quick K-Nearest-Neighbours fit-and-predict.  The model is trained
    and evaluated on the same data – good enough for the demo.
    """
    if not isinstance(parcel, dict) or "data" not in parcel:
        raise TypeError("Expecting the running-parcel dict with a 'data' key")

    df: pd.DataFrame = parcel["data"]

    # -------- prepare X and y --------
    if label_column and label_column in df.columns:
        X = df.drop(columns=[label_column]).to_numpy()
        y = df[label_column].to_numpy()
    else:                               # no ground-truth labels available
        X = df.to_numpy()
        y = np.arange(len(df))          # dummy labels so KNN can fit

    # -------- train & predict --------
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X, y)
    df["predicted_label"] = knn.predict(X)

    parcel["data"] = df                 # update and return the same parcel
    return parcel
