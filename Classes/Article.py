from pymongo.collection import Collection

class Article:
    def __init__(self, title, content, date_published, author, source): 
        self.title = title  
        self.content = content
        self.date_published = date_published
        self.author = author
        self.source = source
        self.sentiment_score = None  
        self.keywords = []  

    def to_dict(self):
        """Convert the Article instance to a dictionary for MongoDB insertion."""
        return {
            "title": self.title,
            "content": self.content,
            "date_published": self.date_published,
            "author": self.author,
            "source": self.source,
            "sentiment_score": self.sentiment_score,
            "keywords": self.keywords
        }

    @staticmethod
    def insert_articles_to_db(articles: list['Article'], collection: Collection):
        collection.insert_many([article.to_dict() for article in articles])

    @staticmethod
    def insert_article_to_db(article: 'Article', collection: Collection):
        collection.insert_one(article.to_dict())
