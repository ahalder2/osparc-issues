import json
import os
from pathlib import Path

import attr
import click
from yarl import URL

# pylint: disable=wildcard-import,unused-wildcard-import
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


team = [Member(name, short) for name, short in zip(MEMBERS[::2], MEMBERS[1::2])]


@click.group()
@click.option(
    "--token",
    default=None,
    help="github api token. To get a personal token, visit https://github.com/settings/tokens and log in.",
)
def main(token=None):
    if token:
        cache_headers(token)
        click.echo("Token cached")

    if HEADER_CACHE.exists():
        click.echo(f"Cached token {HEADER_CACHE}")


@main.command()
def pull_and_dump():
    click.echo("pull_and_dump")

    os.makedirs(".cache", exist_ok=True)

    columns = get_project_columns()
    with open(".cache/columns.json", "wt") as fh:
        json.dump(columns, fh, indent=2)

    # finds cases in progress
    in_progress = next(c["id"] for c in columns if c["name"] == "Dev - In progress")

    # dump issues in progres
    issues = get_issues_in_column(in_progress)
    with open(".cache/in_progress.json", "wt") as fh:
        json.dump(issues, fh, indent=2)

    # find cases scheduled
    scheduled = next(c["id"] for c in columns if c["name"] == "Scheduled")

    # dump issues scheduled
    issues = get_issues_in_column(scheduled)
    with open(".cache/scheduled.json", "wt") as fh:
        json.dump(issues, fh, indent=2)


@main.command()
@click.option("--output", default="draft-agenda.md", help="output markdown")
def agenda(output: Path):
    """ Produces a markdown with an agenda for the review meeting
    """
    click.echo(f"agenda -> {output}")
    # TODO: determine current items
    # cs = Sprint(, )
    # cm = Meeting()

    # rerder agenda

    # render_markdown_doc(output_md, meeting=cm, sprint=cs, team=team)


@main.command()
def clean():
    """ Cleans cache
    """
    click.echo("Cleaning cache ...")
    clear_cache()


if __name__ == "__main__":
    main()
