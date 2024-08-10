from typing import List
import pandas as pd
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from pmbuddy.models import PubmedArticle
from pmbuddy.util import format_name


def display_table(df: pd.DataFrame, console: Console) -> None:
    # Tidy up fields and filter columns
    df["pub_year"] = df["pub_year"].astype(str)
    df["pub_month"] = df["pub_month"].astype(str)
    df["authors"] = df["authors"].apply(lambda names: map(format_name, names))
    df["authors"] = df["authors"].apply(lambda l: ", ".join(map(str, l)))
    subset = ["pmid", "title", "journal", "pub_year", "pub_month", "authors"]
    df_filtered = df[subset]
    # Create Rich table
    table = Table(title="PubMed Articles", box=box.SIMPLE_HEAVY, expand=True)
    table.add_column(justify="center")
    for col in df_filtered.columns:
        table.add_column(col, justify="left")
    for url, (idx, row) in zip(df["url"], df_filtered.iterrows()):
        pmid, title, authors, journal, *remaining = list(row)
        table.add_row(
            str(idx + 1),
            f"[cyan][link={url}]{pmid}",
            f"[b]{title}",
            authors,
            f"[i]{journal}",
            *remaining,
        )
    console.print(table)


def display_abstract(articles: List[PubmedArticle], console: Console) -> None:
    for article in articles:
        abstract = Text(article.abstract, justify="full")
        authors = ", ".join(article.authors)
        title = Text(article.title, justify="full")
        title.stylize("bold cyan")
        title_panel = Panel(
            Align(title, "center"), subtitle=authors, subtitle_align="center"
        )
        abstract.pad_left(10)
        panel = Panel(
            abstract,
            box=box.SIMPLE_HEAVY,
            subtitle=article.url,
            subtitle_align="center",
            padding=[1, 15, 2, 15],
        )
        console.print(title_panel)
        console.print(panel)


def display_abstract_panel(articles: List[PubmedArticle], console: Console) -> None:
    HEIGHT = 25
    layouts = []
    for idx, article in enumerate(articles, start=1):
        abstract = Align.center(
            Text(article.abstract, justify="full"), vertical="middle"
        )
        authors = Text(f"{article.authors[0]} et al.", style="italic")
        title = Align.center(
            Text(article.title.upper(), justify="center", style="bold cyan"),
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
