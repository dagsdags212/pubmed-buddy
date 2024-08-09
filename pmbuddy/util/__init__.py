from pathlib import Path
from typing import List, Optional
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from pmbuddy.data import CONFIG
from pmbuddy.util.validation import validate_pmid, validate_pmcid
from pmbuddy.models import PubmedArticle


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

def detect_article_source(url: str) -> Optional[str]:
    scheme, domain, *_ = Path(url).parts
    match domain:
        case "www.ncbi.nlm.nih.gov":
            return "PUBMED"
        case "www.nature.com":
            return "NATURE"
        case _:
            print("Cannot identify URL source")
            return

def extract_text(
    parent: Tag,
    tag: str,
    class_: Optional[str] = None,
    id: Optional[str] = None) -> str:
    if id:
        try:
            text = parent.find(tag, id=id).text.strip()
        except AttributeError:
            text = "Text not available"
    elif class_:
        try:
            text = parent.find(tag, class_=class_).text.strip()
        except AttributeError:
            text = "Text not available"
    else:
        try:
            text = parent.find(tag).text.strip()
        except AttributeError:
            text = "Text not available"
    return text

def extract_node(parent: Tag, tag: str, class_: Optional[str] = None, id: Optional[str] = None):
    """Find the first child node of given parent, tag, and identifier."""
    if id:
        return parent.find(tag, id=id)
    elif class_:
        return parent.find(tag, class_=class_)
    return parent.find(tag)

def extract_nodes(parent: Tag, tag: str, class_: Optional[str] = None, id: Optional[str] = None):
    """Find a list of children nodes from a given parent, tag, and identifier."""
    if id:
        return parent.find_all(tag, id=id)
    elif class_:
        return parent.find_all(tag, class_=class_)
    return parent.find_all(tag)

def fetch_articles(parser, pmids: List[str]) -> List[PubmedArticle]:
    """Fetch journal metadata from a list of PubMed identifiers."""
    return [parser.fetch_article(pmid) for pmid in pmids]

def serialize(filepath) -> str:
    pmid_list = []
    try:
        with open(filepath, "r") as handle:
            for pmid in handle.readlines():
                pmid_list.append(pmid.strip())
        return pmid_list
    except FileNotFoundError as e:
        raise e

def format_name(name: str) -> str:
    """Only include the last name, followed by the first letter of the first name.

    Example:
        >>> name = "Steve Jobs"
        >>> print(format_name(name))
        Jobs S
    """
    name_comps = name.split(" ")
    return f"{name_comps[-1]} {name_comps[0][0]}"
