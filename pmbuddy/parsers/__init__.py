from pmbuddy.parsers.Pubmed import PubmedParser


class ArticleParser:
    @staticmethod
    def fetch_from_url(url: str):
        parser = PubmedParser()
        article = parser.fetch_article(url)
        return article
