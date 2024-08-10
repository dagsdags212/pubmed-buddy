from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pmbuddy.config import CONFIG


class PublicationDate(BaseModel):
    year: int
    month: int | str
    day: Optional[int] = None


class PageRange(BaseModel):
    start: int
    end: int

    @property
    def span(self) -> int:
        return self.end - self.start


class Citation(BaseModel):
    journal: str
    publication_date: PublicationDate
    doi: str
    issue_num: Optional[int] = None
    article_num: Optional[str] = None
    pages: Optional[PageRange] = None


class Article(BaseModel):
    title: str
    authors: List[str]
    citation: Citation
    abstract: Optional[str] = None

    def json(self) -> Dict[str, Any]:
        """Flattens article metadata into JSON format."""
        return {
            "title": self.title,
            "authors": self.authors,
            "journal": self.citation.journal,
            "pub_month": self.citation.publication_date.month,
            "pub_year": self.citation.publication_date.year,
            "article_num": self.citation.article_num,
            "issue_num": self.citation.issue_num,
            "doi": self.citation.doi,
        }


class PubmedArticle(Article):
    pmcid: str
    pmid: str

    @property
    def url(self) -> str:
        return f"{CONFIG['urls']['PMID_ROOT']}/{self.pmid}/"

    def json(self) -> Dict[str, Any]:
        """Flattens article metadata into JSON format."""
        return {
            "title": self.title,
            "authors": self.authors,
            "pmcid": self.pmcid,
            "pmid": self.pmid,
            "journal": self.citation.journal,
            "pub_month": self.citation.publication_date.month,
            "pub_year": self.citation.publication_date.year,
            "article_num": self.citation.article_num,
            "issue_num": self.citation.issue_num,
            "doi": self.citation.doi,
            "url": f"{CONFIG['urls']['PMID_ROOT']}/{self.pmid}/",
        }
