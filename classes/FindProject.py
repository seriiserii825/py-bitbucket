import csv
import glob
import os
from typing import List

from utils import pretty_print, pretty_table


class FindProject:
    """Searches a repo name (substring, case-insensitive) in all cached CSVs."""

    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.start()

    def start(self):
        query = input("Enter part of the repo name: ").strip().lower()
        if not query:
            pretty_print("Search query cannot be empty.", error=True)
            return

        rows = [row for row in self._collect_repos() if query in row[0].lower()]
        if not rows:
            pretty_print(f"No repos found matching '{query}'.", error=True)
            return

        rows.sort(key=lambda row: (row[0].lower(), row[1]))
        pretty_table(f"Found {len(rows)} repo(s) for '{query}'", ["Repo", "Git", "Location"], rows)

    def _collect_repos(self) -> List[List[str]]:
        rows: List[List[str]] = []

        for record in self._read_csv("github_repos.csv"):
            rows.append([record["Name"], "[green]GitHub", "seriiserii825"])

        for record in self._read_csv("forgejo_repos.csv"):
            owner, _, name = record["FullName"].partition("/")
            rows.append([name, "[magenta]Forgejo", owner])

        for path in glob.glob(os.path.join(self.ROOT_DIR, "*@*_repos.csv")):
            email = os.path.basename(path).removesuffix("_repos.csv")
            for record in self._read_csv(path):
                rows.append([record["Name"], "[blue]Bitbucket", f"{record['Workspace']} ({email})"])

        return rows

    def _read_csv(self, file_name: str) -> List[dict]:
        path = os.path.join(self.ROOT_DIR, file_name)
        if not os.path.exists(path):
            pretty_print(f"{os.path.basename(path)} not found, skipping.", error=True)
            return []
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
