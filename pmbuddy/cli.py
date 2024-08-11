import argparse
from pathlib import Path
import subprocess
from typing import List, Tuple
import pandas as pd
from rich.console import Console
from rich.layout import Layout
from pmbuddy.models import PubmedArticle
from pmbuddy.parsers import ArticleParser, Pubmed
from pmbuddy.util import serialize
from pmbuddy.util.requests import fetch_articles
from pmbuddy.util.display import (
    display_multiple_abstracts,
    display_single_abstract,
    display_table,
)


def to_dataframe(articles: List[PubmedArticle]) -> pd.DataFrame:
    data = [a.json() for a in articles]
    return pd.DataFrame(data)


parser = argparse.ArgumentParser(
    prog="pubmed-buddy", description="Streamline retrival of journal data from PubMed"
)

parser.add_argument("--pmid", "-i", action="store", help="PubMed journal identifier")

parser.add_argument("--abstract", action="store_true", help="display article abstract")

parser.add_argument(
    "--file", "-f", help="provide filepath containing PMIDs separated by newlines"
)


def main() -> None:
    args = parser.parse_args()
    if args.file:
        pmid_list = serialize(args.file)
        n_articles = len(pmid_list)
        pmid_str = ",".join(pmid_list)
    elif args.pmid:
        pmid_str = args.pmid
        n_articles = len(pmid_str.split(","))
    else:
        raise ValueError

    tmp_data = Path("/tmp/pubmed_data.csv")
    spider = Path(__file__).parent / "spider.py"
    subprocess.call(f"python {str(spider)} {pmid_str}", shell=True)
    # Load scraped data into a dataframe.
    df = pd.read_csv(tmp_data)
    df[["pub_year", "pub_month"]] = df["pubdate"].str.split(",", n=1, expand=True)
    subset = ["pmid", "title", "authors", "journal"]
    console = Console()
    if args.abstract:
        if n_articles > 1:
            display_multiple_abstracts(df, console)
        else:
            display_single_abstract(df, console)
    else:
        display_table(df, subset, console)
    exit(0)
