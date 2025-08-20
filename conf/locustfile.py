import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from locust import HttpUser, task

LOCUST_FILENAME = os.getenv("LOCUST_FILENAME", "conf/bigbrain.txt")
LOCUST_TARGET = os.getenv("LOCUST_TARGET")

@dataclass
class Target:
    name: str
    includes: list[str]
    excludes: list[str]


target_dictionaries = [
    Target(
        name="siibra-explorer",
        includes=[
            "https://atlases.ebrains.eu/viewer"
        ],
        excludes=[]
    ),
    Target(
        name="siibra-api",
        includes=[
            "https://siibra-api.apps."
        ],
        excludes=[
            "&bbox="
        ]
    ),
    Target(
        name="data-vm",
        includes=[
            "https://neuroglancer.humanbrainproject.eu"
        ],
        excludes=[]
    )
]


exceptions = (
    "https://stackpath",
    "https://cdn.plot.ly"
)

with open(LOCUST_FILENAME, "r") as fp:
    urls_txt = fp.read()

urls = [u
        for u in urls_txt.split("\n")
        if (
            u != ""
            or any(u.startswith(ex) for ex in exceptions)
            or not u.startswith("https")
            )]

class SiibraExplorerUser(HttpUser):

    def on_start(self):
        global urls

        use_dictionary = None
        for d in target_dictionaries:
            if d.name == LOCUST_TARGET:
                use_dictionary = d
                break
        
        if use_dictionary is None:
            return
        
        urls = [u
                for u in urls
                if (
                    any(incl in u for incl in use_dictionary.includes)
                    and all(excl not in u for excl in use_dictionary.excludes)
                )]

    @task
    def bigbrain_zoomin(self):
        def get(url: str):
            resp = self.client.get(url)
            return resp.content
        with ThreadPoolExecutor(max_workers=6) as ex:
            list(
                ex.map(
                    get,
                    urls
                )
            )
        # quits once all of the content are retrieved once
        self.environment.runner.quit()
