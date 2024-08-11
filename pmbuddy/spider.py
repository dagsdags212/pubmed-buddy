from typing import Optional, List, Tuple
from pathlib import Path
import re
from pmbuddy.util import generate_urls_from_ids
import scrapy
from scrapy import Field, Item
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from pmbuddy.config import CONFIG


Pubdate = Tuple[str | int, str | int]


def extract_pubdate_from_citation(citation: str) -> Pubdate:
    pubdate_regex = r"(\d{4})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+"
    year, month = re.findall(pubdate_regex, citation.strip())[0]
    return year, month


class PubmedArticle(Item):
    pmid = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(str.strip))
    authors = Field()
    journal = Field()
    doi = Field(input_processor=MapCompose(str.strip))
    abstract = Field(input_processor=MapCompose(str.strip))
    pmcid = Field()
    pubdate = Field(input_processor=MapCompose(extract_pubdate_from_citation))


class PubmedSpider(scrapy.Spider):
    name = "pubmed"
    start_urls = generate_urls_from_ids([39111311, 39101671, 39106859])

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        feeds = {
            "/tmp/pubmed_data.csv": {
                "format": "csv",
                "encoding": "utf8",
                "overwrite": True,
            }
        }
        settings.set("FEEDS", feeds, priority="spider")
        settings.set("LOG_LEVEL", "DEBUG", priority="spider")
        settings.set("LOG_FILE", "/tmp/pmbuddy", priority="spider")

    def parse(self, response):
        article = ItemLoader(item=PubmedArticle(), response=response)
        article.add_css("title", "title::text")
        article.add_css("journal", "div.article-citation span.journal::text")
        article.add_css("abstract", "div#abstract p::text")
        article.add_css("authors", "div.authors-list a.full-name::text")
        article.add_css("pmid", "a.id-link::text")
        article.add_css("pmcid", "strong.current-id::text")
        article.add_css("pubdate", "span.cit::text")
        article.add_css("doi", "span.citation-doi::text")
        return article.load_item()


if __name__ == "__main__":
    from sys import argv

    pmid_list = argv[1].split(",")
    process = CrawlerProcess()
    PubmedSpider.start_urls = generate_urls_from_ids(pmid_list)
    process.crawl(PubmedSpider)
    process.start()
