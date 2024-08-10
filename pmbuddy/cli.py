import argparse
from typing import List, Tuple
import pandas as pd
from rich.console import Console
from rich.layout import Layout
from pmbuddy.models import PubmedArticle
from pmbuddy.parsers import ArticleParser, Pubmed
from pmbuddy.util import serialize
from pmbuddy.util.requests import fetch_articles
from pmbuddy.util.display import display_table, display_abstract, display_abstract_panel


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
    ap = ArticleParser()
    console = Console()
    args = parser.parse_args()
    articles = None

    pmid_list = None
    if args.file:
        pmid_list = serialize(args.file)
    elif args.pmid:
        if "," in args.pmid:
            pmid_list = args.pmid.split(",")
        else:
            pmid_list = [args.pmid]
    else:
        raise ValueError

    articles = fetch_articles(ap, pmid_list)

    if args.abstract:
        if len(articles) > 1:
            display_abstract_panel(articles, console)
        else:
            display_abstract(articles, console)
    else:
        df = to_dataframe(articles)
        display_table(df, console)
