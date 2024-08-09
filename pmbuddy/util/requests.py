from typing import List
import httpx
from bs4 import BeautifulSoup
from pmbuddy.models import PubmedArticle
from pmbuddy.config import CONFIG
from pmbuddy.util.validation import validate_pmid, validate_pmcid


def soup_from_url(url: str) -> BeautifulSoup:
    """Return a soup object from a URL string."""
    global CONFIG
    res = None
    with httpx.Client() as client:
        req_params = CONFIG.get("request")
        if req_params:
            res = client.get(url, headers=req_params.get("headers"), timeout=req_params.get("timeout", 5.0))
        else:
            res = client.get(url, timeout=5.0)
        res.raise_for_status()
    return BeautifulSoup(res.content, "html.parser")

def soup_from_pmid(pmid: str) -> BeautifulSoup:
    pmid = validate_pmid(pmid)
    url = f"{CONFIG['urls']['PMID_ROOT']}/{pmid}/"
    return soup_from_url(url)

def soup_from_pmcid(pmcid: str) -> BeautifulSoup:
    pmcid = validate_pmcid(pmcid)
    url = f"{CONFIG['urls']['PMCID_ROOT']}/{pmcid}/"
    return soup_from_url(url)

def fetch_articles(parser, pmids: List[str]) -> List[PubmedArticle]:
    """Fetch journal metadata from a list of PubMed identifiers."""
    articles = []
    for pmid in pmids:
        try:
            a = parser.fetch_article(pmid)
            articles.append(a)
        except AttributeError:
            print(f"Failed to parse article metadata. Skipping {pmid}")
            continue
    return articles
