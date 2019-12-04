import json
import sys
from pprint import pprint
from typing import Dict, List

import attr
import requests
from yarl import URL



MEMBERS = "odeimaiz OM ignapas IP mguidon MaG pcrespov PC KZzizzle KZ sanderegg SAN".split()

## https://developer.github.com/v3/projects/#list-organization-projects
ORIGIN = "https://api.github.com"
OWNER = "ITISFoundation"


# BACKLOG ITEMS
# https://github.com/orgs/ITISFoundation/projects/3
PROJECT_ID = "1234240"


def dump_headers(token):
    header = {
      'Authorization': f'token {token}',
      'Accept': 'application/vnd.github.inertia-preview+json'
    }
    with open('.header.json', 'wt') as fh:
      json.dump(header, fh)

def headers():
    with open('.header.json', 'wt') as fh:
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


def get_project_columns():
  # https://developer.github.com/v3/projects/columns/#list-project-columns
  url = f"{ORIGIN}/projects/{PROJECT_ID}/columns"
  res = requests.get(url, headers=headers())
  return res.json()


def get_project_table():
  # urls
  projects_url = f"{ORIGIN}/orgs/{OWNER}/projects"

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

]