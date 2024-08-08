import argparse
from typing import List
import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
from pmbuddy.parsers import ArticleParser


parser = argparse.ArgumentParser(
    prog="pubmed-buddy",
    description="Streamline retrival of journal data from PubMed"
)

parser.add_argument(
    "--pmid", "-i", action="store",
    help="PubMed journal identifier"
)

parser.add_argument(
    "--abstract", action="store_true",
    help="display article abstract"
)

def to_dataframe(parser: ArticleParser, pmids: List[str]) -> pd.DataFrame:
    data = []
    for pmid in pmids:
        article = parser.fetch_article(pmid)
        data.append(article.json())
    return pd.DataFrame(data)

def display_rich_table(df: pd.DataFrame) -> None:
    # Tidy up fields and filter columns
    df["pub_year"] = df["pub_year"].astype(str)
    df["pub_month"] = df["pub_month"].astype(str)
    df["pages"] = (df["end_page"] - df["start_page"]).astype(str)
    df["authors"] = df["authors"].apply(lambda l: ", ".join(map(str, l)))
    subset = ["pmid", "title", "authors", "journal", "pub_year", "pub_month"]
    df_filtered = df[subset]
    # Create Rich table
    table = Table(title="PubMed Articles", box=box.SIMPLE_HEAVY, expand=True)
    table.add_column(justify="center")
    for col in df_filtered.columns:
        table.add_column(col, justify="left")
    for url, (idx, row) in zip(df["url"], df_filtered.iterrows()):
        pmid, title, authors, journal, *remaining = list(row)
        table.add_row(
            str(idx+1),
            f"[cyan][link={url}]{pmid}",
            f"[b]{title}",
            authors,
            f"[i]{journal}",
            *remaining)
    console.print(table)

ap = ArticleParser()
console = Console()

def main() -> None:
    args = parser.parse_args()
    if args.pmid:
        if "," in args.pmid:
            pmid_list = args.pmid.split(",")
            df = to_dataframe(ap, pmid_list)
            display_rich_table(df)
        else:
            article = ap.fetch_article(args.pmid)
            print(article.json())
