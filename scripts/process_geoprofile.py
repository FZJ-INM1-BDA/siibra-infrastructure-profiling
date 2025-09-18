import sys
from pathlib import Path
import re
from collections import defaultdict
import json
from typing import List, Dict

import pandas as pd

GEOPROFILE_DATAVM_RE = re.compile(r"geoprofile-datavm-[0-9a-f]+/linode-(?P<georegion>[a-z-]+)-0/output_stats.csv")
GEOPROFILE_SAPI_RE = re.compile(r"geoprofile-siibraapi-[0-9a-f]+/linode-(?P<georegion>[a-z-]+)-0/output_stats.csv")
GEOPROFILE_SXPLR_RE = re.compile(r"geoprofile-siibraexplorer-[0-9a-f]+/linode-(?P<georegion>[a-z-]+)-0/output_stats.csv")

class TimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, pd.Timestamp):
            return o.strftime('%Y-%m-%d %X')
        return super().default(o)

def main(path: str, *args):
    output_arr = []
    patterns = [GEOPROFILE_DATAVM_RE, GEOPROFILE_SAPI_RE, GEOPROFILE_SXPLR_RE]
    labels = ["datavm", "siibraapi", "siibraexplorer"]
    for label, pattern in zip(labels, patterns):

        metadata_collection = {}
        print(f"{label} :")
        for region, (avg, std, n, metadata) in collate(path, pattern=pattern).items():
            print(f"   {region}: {avg} ({std}) {n=}")
            output_arr.append({
                "label": label,
                "region": region,
                "avg": avg,
                "std": std,
                "unit": "ms",
                "n": n
            })
            assert region not in metadata_collection
            metadata_collection[region] = metadata
        print("-----------")

        for region, metadata_arr in metadata_collection.items():
            path_to_file = Path(f"reports/geoprofile_{label}_raw/{region}.metadata.json")
            path_to_file.parent.mkdir(exist_ok=True, parents=True)
            with open(path_to_file, "w") as fp:
                json.dump(metadata_arr, indent=2, fp=fp, cls=TimeEncoder)
                fp.write("\n")

    with open(f"reports/geoprofile.json", "w") as fp:
        json.dump(output_arr, indent=2, fp=fp)
        fp.write("\n")


def get_metadata(csv_path: Path):

    jsonoutput = csv_path.with_name("output.json")
    
    df = pd.read_json(jsonoutput)
    start_time = df["start_time"].min()
    end_time = (df["start_time"] + pd.to_timedelta(df["total_response_time"])).max()
    return {
        "start": start_time,
        "end": end_time,
        "raw_json": str(jsonoutput),
        "csv_path": str(csv_path),
    }


def collate(path: str, *args, pattern: re.Pattern):
    georegion_dict: Dict[str, List[Path]] = defaultdict(list)
    for f in Path(path).glob("**/*"):
        relative_path = f.relative_to(path)
        matched = pattern.match(str(relative_path))

        # shortcircuit early
        if not matched:
            continue
        
        georegion, = matched.groups()
        georegion_dict[georegion].append(f)
    
    rtn_dict = {}
    for georegion, filelist in georegion_dict.items():
        medians: List[float] = []
        median_metadata = []
        _df = None
        for f in filelist:
            df = pd.read_csv(f)
            _idx, row = list(df.iterrows())[-1]
            median = float(row["Median Response Time"])
            medians.append(median)
            median_metadata.append({
                "median": median,
                **get_metadata(f),
            })
        _df = pd.Series(medians)
        rtn_dict[georegion] = (_df.mean(), _df.std(), int(_df.count()), median_metadata)
    return rtn_dict
        

if __name__ == "__main__":
    main(*sys.argv[1:])
