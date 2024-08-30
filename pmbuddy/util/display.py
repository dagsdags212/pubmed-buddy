from typing import List

import pandas as pd
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from pmbuddy.config import CONFIG
from pmbuddy.models import PubmedArticle
from pmbuddy.util import format_name


def display_table(df: pd.DataFrame, subset: List[str], console: Console) -> None:
    # Tidy up fields and filter columns
    df["authors"] = df["authors"].apply(
        lambda names: map(format_name, names.split(","))
    )
    df["authors"] = df["authors"].apply(lambda l: ", ".join(map(str, l)))
    # Create Rich table
    table = Table(title="PubMed Articles", box=box.SIMPLE_HEAVY, expand=True)
    table.add_column(justify="center")
    df = df[subset]
    for col in df.columns:
        table.add_column(col, justify="left")
    for idx, row in df.iterrows():
        pmid, title, authors, journal, *remaining = row.values
        table.add_row(
            str(idx + 1),
            f"[cyan link={CONFIG['urls']['PMID_ROOT']}/{pmid}]{pmid}",
            f"[b]{title}",
            authors,
            f"[i]{journal}",
        )
    console.print(table)


def display_single_abstract(df: pd.DataFrame, console: Console) -> None:
    df = df[["title", "authors", "abstract", "doi"]]
    for idx, row in df.iterrows():
        abstract = Text(row.abstract, justify="full")
        authors = row.authors
        title = Text(row.title, justify="full")
        title.stylize("bold cyan")
        title_panel = Panel(
            Align(title, "center"), subtitle=authors, subtitle_align="center"
        )
        abstract.pad_left(10)
        panel = Panel(
            abstract,
            box=box.SIMPLE_HEAVY,
            subtitle=row.doi,
            subtitle_align="center",
            padding=[1, 15, 2, 15],
        )
        console.print(title_panel)
        console.print(panel)


def display_multiple_abstracts(df: pd.DataFrame, console: Console) -> None:
    df = df[["title", "authors", "abstract"]]
    HEIGHT = 25
    layouts = []
    for idx, row in df.iterrows():
        abstract = Align.center(Text(row.abstract, justify="full"), vertical="middle")
        authors = Text(f"{row.authors.split(',')[0]} et al.", style="italic")
        title = Align.center(
            Text(row.title.upper(), justify="center", style="bold cyan"),
            vertical="middle",
        )
        abstract_panel = Panel(abstract, box=box.SIMPLE_HEAVY, height=HEIGHT)
        title_panel = Panel(
            title, height=HEIGHT, subtitle=authors, subtitle_align="center"
        )
        layout = Layout()
        left_name = f"title{idx}"
        right_name = f"abstract{idx}"
        layout.size = None
        layout.minimum_size = 10
        layout.split_row(
            Layout(name=left_name),
            Layout(name=right_name),
        )
        layout[right_name].ratio = 2
        layout[left_name].update(title_panel)
        layout[right_name].update(abstract_panel)
        layouts.append(layout)
    main_layout = Layout()
    main_layout.split_column(*layouts)
    console.print(main_layout)
