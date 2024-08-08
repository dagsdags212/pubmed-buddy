from pathlib import Path
from typing import List, Optional
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from pmbuddy.data import CONFIG
from pmbuddy.helpers.validation import validate_pmid, validate_pmcid


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
        return parent.find(tag, id=id).text.strip()
    elif class_:
        return parent.find(tag, class_=class_).text.strip()
    return parent.find(tag).text.strip()

def extract_node(parent: Tag, tag: str, class_: Optional[str] = None, id: Optional[str] = None):
    if id:
        return parent.find(tag, id=id)
    elif class_:
        return parent.find(tag, class_=class_)
    return parent.find(tag)

def extract_nodes(parent: Tag, tag: str, class_: Optional[str] = None, id: Optional[str] = None):
    if id:
        return parent.find_all(tag, id=id)
    elif class_:
        return parent.find_all(tag, class_=class_)
    return parent.find_all(tag)
