import json
from pathlib import Path
from typing import Dict, List

import requests

MEMBERS = "odeimaiz OM ignapas IP mguidon MaG pcrespov PC KZzizzle KZ sanderegg SAN Surfict ALL".split()

## https://developer.github.com/v3/projects/#list-organization-projects
ORIGIN = "https://api.github.com"
OWNER = "ITISFoundation"


# BACKLOG ITEMS
# https://github.com/orgs/ITISFoundation/projects/3
PROJECT_ID = "1234240"


HEADER_CACHE = Path("~/.github-api-header.json").expanduser()

def cache_headers(token: str):
    header = {
      'Authorization': f'token {token}',
      'Accept': 'application/vnd.github.inertia-preview+json'
    }
    with open(HEADER_CACHE, 'wt') as fh:
        json.dump(header, fh)

def clear_cache():
    if HEADER_CACHE.exists():
        HEADER_CACHE.unlink()

def headers() -> Dict:
    with open(HEADER_CACHE, 'rt') as fh:
        return json.load(fh)


def get_issue(repo_name, issue_number) -> Dict:
    # https://developer.github.com/v3/issues/#get-a-single-issue
    url = f"{ORIGIN}/repos/{OWNER}/{repo_name}/issues/{issue_number}"
    res = requests.get(url, headers=headers())
    issue = res.json()
    return issue


def get_issues_in_column(column_id) -> List[Dict]:
    ## https://developer.github.com/v3/projects/cards/#list-project-cards
    issues = []
    url = f"{ORIGIN}/projects/columns/{column_id}/cards"

    res = requests.get(url, headers=headers)
    cards = res.json()
    for card in cards:
        res = requests.get(card["content_url"], headers=headers)
        issue = res.json()
        issues.append(issue)

    return issues


def get_project_columns() -> Dict:
    # https://developer.github.com/v3/projects/columns/#list-project-columns
    url = f"{ORIGIN}/projects/{PROJECT_ID}/columns"
    res = requests.get(url, headers=headers())
    return res.json()


def get_project_table() -> Dict:
    # urls
    ## projects_url = f"{ORIGIN}/orgs/{OWNER}/projects"

    columns_url = f"{ORIGIN}/projects/{PROJECT_ID}/columns"

    hds = headers()

    table = {}
    res = requests.get(columns_url, headers=hds)
    for col in res.json():
        table[col['name']] = []
        res = requests.get(col['cards_url'], headers=hds)
        for card in res.json():
            table[col['name']].append(card)

    return table




__all__ = [
    'MEMBERS',
    'get_issues_in_column',
    'get_project_columns',
    'cache_headers',
    'clear_cache',
    'HEADER_CACHE'
]
