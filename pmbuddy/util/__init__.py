from pathlib import Path
from typing import List, Optional
from bs4.element import Tag
from pmbuddy.config import CONFIG
from pmbuddy.models import PubmedArticle


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

def serialize(filepath) -> List[str]:
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
