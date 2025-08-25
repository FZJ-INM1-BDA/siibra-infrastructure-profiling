import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main(path_to_timing_json: str, *args):
    df = pd.read_json(path_to_timing_json)
    datavm_rows = df[df["url"].str.contains("https://neuroglancer.humanbrainproject.eu")]
    siibraapi_rows = df[df["url"].str.contains("https://siibra-api.apps.ebrains")]
    siibraexplorer_rows = df[df["url"].str.contains("https://atlases.ebrains.eu/viewer")]
    delta: pd.Timedelta = df['timestamp'].max() - df['timestamp'].min()
    max_seconds = int(delta.seconds) + 2
    bins = pd.cut(df['timestamp'] - df['timestamp'].min() + pd.Timedelta(milliseconds=1),
                  [pd.Timedelta(seconds=i) for i in range(max_seconds)],
                  labels=[f"{i} sec" for i in range(max_seconds - 1)])

    df["bins"] = bins

    datavm_rows = df[df["url"].str.contains("https://neuroglancer.humanbrainproject.eu")]
    siibraapi_rows = df[df["url"].str.contains("https://siibra-api.apps.ebrains")]
    siibraexplorer_rows = df[df["url"].str.contains("https://atlases.ebrains.eu/viewer")]

    labels=["datavm", "siibra-api", "siibra-explorer"]

    ax = plt.axes()
    for _df in datavm_rows, siibraapi_rows, siibraexplorer_rows:
        count = _df.groupby("bins").count()
        count["url"].plot(ax=ax, xlabel="Time elapsed", ylabel="Number of requests")
    ax.legend(labels)
    
    path_to_timing_json_path = Path(path_to_timing_json)
    figure = plt.gcf()
    figure.savefig(path_to_timing_json_path.with_suffix(".png"))

if __name__ == "__main__":
    main(*sys.argv[1:])
