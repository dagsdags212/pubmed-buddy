from pmbuddy.parsers.Pubmed import PubmedParser


class ArticleParser:
    @staticmethod
    def fetch_article(locator: str):
        parser = PubmedParser()
        if "http" in locator:
            article = parser.fetch_from_url(locator)
        else:
            article = parser.fetch_from_id(locator)
        return article
