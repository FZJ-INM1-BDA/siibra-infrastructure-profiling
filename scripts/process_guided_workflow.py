import sys
from pathlib import Path
import re
from collections import defaultdict
import json

import pandas as pd

class TimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, pd.Timestamp):
            return o.strftime('%Y-%m-%d %X')
        return super().default(o)

GUIDED_WORKFLOW_RE = re.compile(r"geoprofile-guided-workflow-[0-9a-f]+/linode-(?P<georegion>[a-z-]+)-0/output.json")

def main(path: str, *args):
    result = collate(path)
    summary_json = []
    for region, (avg, std, n, metadata_arr) in result.items():
        print(f"{region}: {avg} ({std}) {n=}")
        summary_json.append({
            "region": region,
            "avg": avg,
            "std": std,
            "unit": "sec",
            "n": n,
        })
        
        raw_dir = Path("reports/guided_workflow_raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        metapath = raw_dir / f"{region}.metadata.json"
        with open(metapath, "w") as fp:
            json.dump(metadata_arr, indent=2, fp=fp, cls=TimeEncoder)
            fp.write("\n")
    
    with open(f"reports/guided_workflow.json", "w") as fp:
        json.dump(summary_json, indent=2, fp=fp)
        fp.write("\n")


def collate(path: str, *args):
    georegion_dict = defaultdict(list)
    for f in Path(path).glob("**/*"):
        relative_path = f.relative_to(path)
        matched = GUIDED_WORKFLOW_RE.match(str(relative_path))

        # shortcircuit early
        if not matched:
            continue
        georegion, = matched.groups()
        georegion_dict[georegion].append(f)
    
    rtn_dict = {}
    for georegion, filelist in georegion_dict.items():
        totals = []
        _df = None
        metadata_arr = []
        for f in filelist:
            
            df = pd.read_json(f)
            start_time = df["start_time"].min()
            end_time = (df["start_time"] + pd.to_timedelta(df["total_response_time"])).max()
            
            delta: pd.Timedelta  = end_time - start_time
            totals.append(delta.total_seconds())
            metadata_arr.append({
                "start": start_time,
                "end_time": end_time,
                "raw_json": str(f),
                "delta": delta.total_seconds()
            })

        _df = pd.Series(totals)
        rtn_dict[georegion] = (float(_df.mean()), float(_df.std()), int(_df.count()), metadata_arr)
    return rtn_dict

if __name__ == "__main__":
    main(*sys.argv[1:])
