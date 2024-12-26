from pymongo.collection import Collection

class Article:
    def __init__(self, title, content, date_published, author, url): 
        self.title = title  
        self.content = content
        self.author = author
        self.date_published = date_published
        self.url = url

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "date_published": self.date_published,
            "author": self.author,
            "url": self.url,
        }

    
    def get_article_urls_by_ticker(db, ticker):
        try:
            articles = db["articles"].find(
                {"company": ticker}, 
                {"article.url": 1, "_id": 0} 
            )
            
            articles_list = list(articles)
            
            if not articles_list:
                # print(f"No articles found for ticker: {ticker} in the database")
                return None

            # Extract URLs from the result
            urls = [article.get("article", {}).get("url") for article in articles_list if "url" in article.get("article", {})]
            
            return urls
        except Exception as e:
            print(f"Error fetching articles for {ticker}: {e}")
            return None
