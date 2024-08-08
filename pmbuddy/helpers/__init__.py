from pathlib import Path
from typing import List
from typing_extensions import Optional
import httpx
from bs4 import BeautifulSoup
from pmbuddy.data import CONFIG


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
