from fastapi import APIRouter
# Import the news endpoints
from api.endpoints.news import router as news_router
import logging

app = APIRouter()
app.include_router(news_router)

# Include the news router


@app.get("/")
def read_root():
    # Log an info message
    # Log an info message
    logging.info("This is an Home info message.")

    return {"Hello": "World"}
