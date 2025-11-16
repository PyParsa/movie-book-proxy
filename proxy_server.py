import os
import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

app = FastAPI()

# Enable CORS for all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Root
# ---------------------------
@app.get("/")
def home():
    return {"message": "✅ Proxy Server is running successfully on Render!"}

# ---------------------------
# TMDB — Genres
# ---------------------------
@app.get("/tmdb/genres")
async def tmdb_genres(language: str = "en-US"):
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": language}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        return r.json()

# ---------------------------
# TMDB — Discover Movies
# ---------------------------
@app.get("/tmdb/discover")
async def tmdb_discover(
    genre_id: int,
    year: int,
    page: int = 1,
    language: str = "en-US"
):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "primary_release_year": year,
        "language": language,
        "sort_by": "popularity.desc",
        "page": page,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        return r.json()

# ---------------------------
# Google Books — Search
# ---------------------------
@app.get("/books/search")
async def google_books(
    subject: str,
    year: int | None = None,
    max_results: int = 20
):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"subject:{subject}",
        "maxResults": max_results,
        "orderBy": "relevance",
        "key": GOOGLE_BOOKS_API_KEY,
        "printType": "books",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        return r.json()
