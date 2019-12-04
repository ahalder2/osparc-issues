import json
import sys
from pprint import pprint
from typing import Dict, List

import requests
from pytablewriter import MarkdownTableWriter

import attr
from yarl import URL


attr.s(auto_attribs=True)
class Member:
  name: str
  short: str

attr.s(auto_attribs=True)
class Meeting:
  date:
  time:
  agenda_table: str
  nih_deliverables_table: str

attr.s(auto_attribs=True)
class Sprint:
  name: str
  zehnhub_url: URL
  scrum_master: Member



#def create_review_md():
#  with open("review.md", 'wt'):



#---------------

MEMBERS = "odeimaiz OM ignapas IP mguidon MaG pcrespov PC KZzizzle KZ sanderegg SAN".split()
members = [ Member(name, short) for name, short zip(MEMBERS[::2], MEMBERS[1::2]) ]


## https://developer.github.com/v3/projects/#list-organization-projects
ORIGIN = "https://api.github.com"
OWNER = "ITISFoundation"

# https://github.com/orgs/ITISFoundation/projects/3
PROJECT_ID = "1234240"

aouth_token = sys.argv[1]
headers={
  'Authorization': f'token {aouth_token}',
  'Accept': 'application/vnd.github.inertia-preview+json'
}

def get_issue(repo_name, issue_number) -> Dict:
  # https://developer.github.com/v3/issues/#get-a-single-issue
  url = f"{ORIGIN}/repos/{OWNER}/{repo_name}/issues/{issue_number}"
  res = requests.get(url, headers=headers)
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
  res = requests.get(url, headers=headers)
  return res.json()


def get_project_table():
  # urls
  projects_url = f"{ORIGIN}/orgs/{OWNER}/projects"

  columns_url = f"{ORIGIN}/projects/{PROJECT_ID}/columns"

  table = {}
  res = requests.get(columns_url, headers=headers)
  for col in res.json():
    table[col['name']] = []
    res = requests.get(col['cards_url'], headers=headers)
    for card in res.json():
      table[col['name']].append(card)

  return table


def pull_info():
  columns = get_project_columns()
  with open("columns.json", 'wt') as fh:
    json.dump(columns, fh, indent=2)

  in_progress = next(c['id'] for c in columns if c['name']=='Dev - In progress')
  scheduled = next(c['id'] for c in columns if c['name']=='Scheduled')

  issues = get_issues_in_column(in_progress)
  with open("in_progress.json", 'wt') as fh:
    json.dump(issues, fh, indent=2)

  issues = get_issues_in_column(scheduled)
  with open("scheduled.json", 'wt') as fh:
    json.dump(issues, fh, indent=2)


def create_md_table(issues, stream):
    writer = MarkdownTableWriter()
    writer.stream = stream
    writer.headers = ['Issue', 'Title', 'Presenter', 'Status', 'Duration (mins)', 'Time']
    writer.value_matrix = []

    for issue in issues:
        writer.value_matrix.append( [
            "[#{mumber}]({html_url})".format(**issue),
            issue['title'],
            issue['assignee']['login'],
            issue['version'],
            next( label['name'].replace("dev:","") for label in issue['labels'] if label['name'].startswith("dev:")) ,
        ] )

    writer.margin = 2  # add a whitespace for both sides of each cell
    writer.write_table()



def main():
  output_md = sys.argv[2]

  #table = get_project_table()
  #with open("table.json", 'wt') as fh:
  #  json.dump(table, fh, indent=2)

  #pull_info()



if __name__ == "__main__":
  main()
