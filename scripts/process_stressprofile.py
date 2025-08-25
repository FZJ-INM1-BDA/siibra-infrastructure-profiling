import sys
from pathlib import Path
from datetime import datetime


import pandas as pd

def main(path: str, *args):

    stat_history_csv = list(Path(path).glob("**/*_stats.csv"))
    assert len(stat_history_csv) > 0, f"Expected at least one  _stats.csv file, but found none"
    _medsum = []
    for f in stat_history_csv:
        df = pd.read_csv(f)
        _idx, row = list(df.iterrows())[-1]
        med = row["Median Response Time"]
        
        _medsum.append(med)
    _sum = pd.Series(_medsum)
    print(_sum.mean(), _sum.std())


if __name__ == "__main__":
    main(*sys.argv[1:])
