class Article:
    def __init__(self, articleId ,title, content, date_published, author, source):
        
        self.articleId = articleId
        self.title = title  
        self.content = content
        self.date_published = date_published
        self.author = author
        self.source = source
        self.sentiment_score = None  # Placeholder for sentiment analysis result
        self.keywords = []  # List to store extracted keywords

    def analyze_sentiment(self, sentiment_analyzer):
        return self

    def extract_keywords(self, keyword_extractor):
        return self

    def summarize(self, summarizer):
        return self

    def display_info(self):
        """
        Display the article's details in a readable format.
        """
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Date Published: {self.date_published}")
        print(f"Source: {self.source}")
        print(f"Sentiment Score: {self.sentiment_score}")
        print(f"Keywords: {', '.join(self.keywords)}")

