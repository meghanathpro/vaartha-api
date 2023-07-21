from pydantic import BaseModel


class NewsArticleToDb(BaseModel):
    datetime: str
    category: str
    source: str
    content: str
    article_link: str
    image_link: str


class NewsArticleFromDb(BaseModel):
    id: str
    datetime: str
    category: str
    source: str
    content: str
    article_link: str
    image_link: str
