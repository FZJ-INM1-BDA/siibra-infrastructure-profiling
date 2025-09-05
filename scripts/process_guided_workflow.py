import sys
from pathlib import Path

import pandas as pd

def main(path: str, *args):
    outputjson = [f for f in Path(path).glob("**/output.json")]
    assert len(outputjson), f"Expected one and only one output json, but found {len(outputjson)}"
    outputjson, = outputjson

    df = pd.read_json(outputjson)
    start_time = df["start_time"].min()
    end_time = (df["start_time"] + pd.to_timedelta(df["total_response_time"])).max()
    
    delta: pd.Timedelta  = end_time - start_time
    print(delta.total_seconds())

if __name__ == "__main__":
    main(*sys.argv[1:])
