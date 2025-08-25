import sys
from pathlib import Path
from datetime import datetime


import pandas as pd

def main(path: str, *args):

    stat_history_csv = list(Path(path).glob("**/*_stats.csv"))
    assert len(stat_history_csv) ==1, f"Expected one and only one  _stats.csv file, but found {len(stat_history_csv)}"
    df = pd.read_csv(stat_history_csv[0])
    
    _idx, row = list(df.iterrows())[-1]
    med = row["Median Response Time"]
    print(med)


if __name__ == "__main__":
    main(*sys.argv[1:])
