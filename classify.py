"""Small CLI that fetches open issues in a GitHub repo,
sends them to GPT‑4o for P0/P1/P2 labeling, and prints
a color table so we can triage the backlog quickly."""

import argparse, os, sys, json, itertools
from dotenv import load_dotenv
from openai import OpenAI
from github import Github
from rich.console import Console
from rich.table import Table

load_dotenv()
g = Github(os.getenv("GITHUB_TOKEN"))
client = OpenAI()
console = Console()

def fetch_issues(repo_full, limit):
    repo = g.get_repo(repo_full)
    issues = [
        i for i in repo.get_issues(state="open")
        if not i.pull_request
    ]
    return issues[:limit]

def chunk(iterable, n):
    "batch helper"
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch: break
        yield batch

def classify_batch(batch):
    sys_msg = [{
        "role": "system",
        "content": (
            "You are a senior product lead."
            "Label each GitHub issue as P0, P1, or P2."
            "Answer JSON list in same order: [{'number': N, 'priority': 'P0'} ...]."
        )
    }]
    user = {
        "role": "user",
        "content": json.dumps([{"number": i.number,
                                "title": i.title,
                                "body": i.body[:1000]} for i in batch])
    }
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=sys_msg + [user],
        temperature=0
    )
    return json.loads(resp.choices[0].message.content)

def prioritize(repo_full, top_n):
    issues = fetch_issues(repo_full, top_n)
    results = {}
    for batch in chunk(issues, 10):
        for row in classify_batch(batch):
            results[row["number"]] = row["priority"]
    return issues, results

def render(issues, priorities):
    table = Table(title="Issue priorities for "+args.repo)
    table.add_column("Prio", style="bold")
    table.add_column("#")
    table.add_column("Title", overflow="fold")
    for issue in issues:
        prio = priorities.get(issue.number, "?")
        style = {"P0": "red", "P1": "yellow", "P2": "green"}.get(prio, "")
        table.add_row(f"[{style}]{prio}[/{style}]", str(issue.number), issue.title)
    console.print(table)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("repo", nargs="?", default="mendable/firecrawl")
    p.add_argument("--top", type=int, default=50, help="max issues to scan")
    args = p.parse_args()
    issues, prios = prioritize(args.repo, args.top)
    render(issues, prios)