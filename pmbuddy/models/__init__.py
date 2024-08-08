from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


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
    article_num: int
    issue_num: int
    pages: PageRange
    doi: str

class Article(BaseModel):
    title: str
    authors: List[str]
    citation: Citation

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
            "start_page": self.citation.pages.start,
            "end_page": self.citation.pages.end,
            "doi": self.citation.doi,
       }


class PubmedArticle(Article):
    pmcid: str
    pmid: str

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
            "start_page": self.citation.pages.start,
            "end_page": self.citation.pages.end,
            "doi": self.citation.doi,
       }
