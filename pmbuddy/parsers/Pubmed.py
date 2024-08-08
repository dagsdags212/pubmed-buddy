import re
from typing import Tuple, List
from bs4 import BeautifulSoup
from pmbuddy.models import PageRange, PublicationDate, Citation, Article, PubmedArticle
from pmbuddy.helpers import soup_from_url


class PubmedParser:
    """Contains the logic for parsing a Pubmed article."""

    def fetch_article(self, url: str) -> Article:
        soup = soup_from_url(url)
        article = self._parse_soup(soup)
        return article

    def _parse_soup(self, soup) -> Article:
        """Extract metadata from a PubMed article."""
        citation = self._extract_citation(soup)
        pmcid, pmid = self._extract_ids(soup)
        title = self._extract_title(soup)
        authors = self._extract_authors(soup)
        article = PubmedArticle(title=title, authors=authors, citation=citation, pmcid=pmcid, pmid=pmid)
        return article

    def _extract_citation(self, soup: BeautifulSoup) -> Citation:
        """Extract citation fields."""
        # Div containing all citation data
        main_node = soup.find("div", id="mc")
        citation_node = main_node.find("div", class_="citation-default")

        # Divs containing citation fields and journal title
        p1_node = citation_node.find("div", class_="part1")
        pubdate = p1_node.text
        journal = p1_node.find("span").text
        p2_node = citation_node.find("div", class_="part2")
        doi = p2_node.find("a").text

        # Parse citation elements using regex
        regex = r"(\d{4})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec);\s(\d+)\((\d)\):\s(\d+).(\d+)"
        res = re.findall(regex, pubdate)
        year, month, article_num, issue_num, start_page, end_page = res[0]
        pages = PageRange(start=start_page, end=end_page)
        pub_date = PublicationDate(year=year, month=month)
        citation = Citation(journal=journal, publication_date=pub_date,
                            article_num=article_num, issue_num=issue_num,
                            pages=pages, doi=doi)
        return citation

    def _extract_ids(self, soup) -> Tuple[str, str]:
        """Extract PMCID and PMID."""
        id_node = soup.find("div", class_="fm-ids")
        pmcid_node = id_node.find("div", class_="fm-citation-pmcid")
        pmcid = pmcid_node.find("span").find_next_sibling("span").text
        pmid = id_node.find("div", class_="fm-citation-pmid").find("a").text
        return (pmcid, pmid)

    def _extract_title(self, soup) -> str:
        """Extract article title."""
        return soup.find("h1", class_="content-title").text

    def _extract_authors(self, soup) -> List[str]:
        """Extract list of authors."""
        authors_node = soup.find("div", "fm-author")
        authors = []
        for a in authors_node.find_all("a"):
            authors.append(a.text)
        return authors
