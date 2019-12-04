import json

import attr
import click
from pathlib import Path
from yarl import URL

from helpers.data import *
from helpers.doc import *


@attr.s(auto_attribs=True)
class Meeting:
    date: str
    time: str
    agenda_table: str
    nih_deliverables_table: str


@attr.s(auto_attribs=True)
class Member:
    name: str
    short: str

@attr.s(auto_attribs=True)
class Sprint:
    name: str
    zehnhub_url: URL = attr.ib(init=False)
    scrum_master: Member



team = [ Member(name, short) for name, short in zip(MEMBERS[::2], MEMBERS[1::2]) ]


@click.group()
@click.option('--token', default=None, help='github api token')
def main(token):

    # dumps
    if token:
        dump_headers(token)
        click.echo('Token saved')


@main.command()
def pull_and_dump():
    click.echo('pull_and_dump')

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



@main.command()
@click.option('--output', default='draft-agenda.md', help='output markdown')
def agenda(output: Path):
    """ Produces a markdown with an agenda for the review meeting
    """
    click.echo(f'agenda -> {output}')
    # TODO: determine current items
    #cs = Sprint(, )
    #cm = Meeting()

    # rerder agenda

    #render_markdown_doc(output_md, meeting=cm, sprint=cs, team=team)


if __name__ == '__main__':
    main()