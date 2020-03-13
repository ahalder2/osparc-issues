from io import StringIO
from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader
from pytablewriter import MarkdownTableWriter


def create_md_table(issues: Dict) -> str:
    stream = StringIO()
    writer = MarkdownTableWriter()
    writer.stream = stream
    writer.headers = [
        "Issue",
        "Title",
        "Presenter",
        "Status",
        "Duration (mins)",
        "Time",
    ]
    writer.value_matrix = []

    for issue in issues:
        writer.value_matrix.append(
            [
                "[#{mumber}]({html_url})".format(**issue),
                issue["title"],
                issue["assignee"]["login"],
                issue["version"],
                next(
                    label["name"].replace("dev:", "")
                    for label in issue["labels"]
                    if label["name"].startswith("dev:")
                ),
            ]
        )

    writer.margin = 2  # add a whitespace for both sides of each cell
    writer.write_table()
    return stream.getvalue()


def create_markdown(output_path: Path, **kwargs):
    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template("templates/review.md.jinja2")

    with open(output_path) as fh:
        print(template.render(**kwargs), fh)


__all__ = ["create_markdown", "create_md_table"]

