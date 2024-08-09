import re
from typing import Tuple, List
from bs4 import BeautifulSoup
from pmbuddy.models import PageRange, PublicationDate, Citation, Article, PubmedArticle
from pmbuddy.util import (
    extract_text,
    extract_node,
    extract_nodes,
)
from pmbuddy.util.requests import (
    soup_from_url,
    soup_from_pmid,
    soup_from_pmcid,
)

class PubmedParser:
    """Contains the logic for parsing a Pubmed article."""

    def fetch_from_url(self, url: str) -> Article:
        soup = soup_from_url(url)
        article = self._parse_soup(soup)
        return article

    def fetch_from_id(self, id: str) -> Article:
        print("Fetching:", id)
        if id.startswith("PMC"):
            soup = soup_from_pmcid(id)
            article = self._parse_soup(soup)
        else:
            soup = soup_from_pmid(id)
            article = self._parse_soup_overview(soup)
        return article

    def _parse_soup(self, soup) -> Article:
        """Extract metadata from a PubMed article."""
        citation = self._extract_citation(soup)
        pmcid, pmid = self._extract_ids(soup)
        title = extract_text(soup, "h1", class_="content-title")
        authors = self._extract_authors(soup)
        abstract = self._extract_abstract(soup)
        article = PubmedArticle(title=title, authors=authors,
                                citation=citation, pmcid=pmcid,
                                pmid=pmid, abstract=abstract)
        return article

    def _parse_pubdate(self, citation: str) -> List[str]:
        pubdate_regex = r"(\d{4})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+"
        year, month = re.findall(pubdate_regex, citation.strip())[0]
        #regex = r"(\d{4})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*[:;]\s?(.+)\((\d+)\)\D?(\d+)-(\d+)"
        #regex = r"(\d{4})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*;\s?(.+)\((\d)\):\s?(\d+).(\d+)"
        return PublicationDate(year=year, month=month)

    def _parse_soup_overview(self, soup) -> Article:
        # Extract key nodes
        root_node = extract_node(soup, "div", id="article-page")
        abstract_node = extract_node(root_node, "div", id="abstract")
        header_node = extract_node(root_node, "header", id="heading")
        author_list = extract_node(header_node, "div", class_="authors-list")
        # Retrieve text from key nodes
        title = extract_text(header_node, "h1")
        # Citation data
        journal = extract_text(header_node, "button")
        doi = extract_text(header_node, "span", class_="citation-doi")
        authors = [a.text for a in extract_nodes(author_list, "a", class_="full-name")]
        citation_fields = extract_text(header_node, "span", class_="cit")
        pub_date = self._parse_pubdate(citation_fields)
        citation = Citation(journal=journal, publication_date=pub_date,
                            article_num=None, issue_num=None,
                            pages=None, doi=doi)
        # Extract identifiers
        identifier_node = extract_node(header_node, "ul", id="full-view-identifiers")
        pmid = extract_text(identifier_node, "strong", class_="current-id")
        pmcid = extract_text(identifier_node, "a", class_="id-link")
        # Abstract content
        abstract = extract_text(abstract_node, "p")
        article = PubmedArticle(title=title, authors=authors,
                                citation=citation, pmcid=pmcid,
                                pmid=pmid, abstract=abstract)
        return article

    def _extract_citation(self, soup: BeautifulSoup) -> Citation:
        """Extract citation fields."""
        # Div containing all citation data
        main_node = soup.find("div", id="mc")
        citation_node = main_node.find("div", class_="citation-default")

        # Divs containing citation fields and journal title
        p1_node =  extract_node(citation_node, "div", class_="part1")
        citation_fields = p1_node.text
        journal = extract_text(p1_node, "span")
        p2_node = extract_node(citation_node, "div", class_="part2")
        doi = extract_text(p2_node, "a")

        # Parse citation elements using regex
        pub_date = self._parse_citation_fields(citation_fields)
        citation = Citation(journal=journal, publication_date=pub_date,
                            article_num=None, issue_num=None,
                            pages=None, doi=doi)
        return citation

    def _extract_ids(self, soup) -> Tuple[str, str]:
        """Extract PMCID and PMID."""
        id_node = extract_node(soup, "div", class_="fm-ids")
        pmcid_node = extract_node(id_node, "div", class_="fm-citation-pmcid")
        pmcid = pmcid_node.find("span").find_next_sibling("span").text
        pmid = id_node.find("div", class_="fm-citation-pmid").find("a").text
        return (pmcid, pmid)

    def _extract_authors(self, soup) -> List[str]:
        """Extract list of authors."""
        authors_node = extract_node(soup, "div", "fm-author")
        authors = []
        for a in extract_nodes(authors_node, "a"):
            authors.append(a.text)
        return authors

    def _extract_abstract(self, soup) -> str:
        """Extract abstract content."""
        abstract_node = extract_node(soup, "div", id="abstract-a.ab.b.r")
        abstract = extract_text(abstract_node, "p")
        return abstract
