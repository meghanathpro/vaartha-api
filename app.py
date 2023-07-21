from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main import app as api_app
import logging

# Create the FastAPI instance
app = FastAPI()

# Include the API routes
app.include_router(api_app)

# Optional: Add any additional middleware or configuration for the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
# For example, you can add CORS middleware, authentication, etc.
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/app.log",  # Path to the log file inside the 'logs' folder
    filemode="a",
)

if __name__ == "__main__":
    import uvicorn

    # Run the API server using Uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
