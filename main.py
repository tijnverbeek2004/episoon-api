from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from models.title import SearchResult, TitleDetail
from services.tmdb import TmdbService

load_dotenv()

app = FastAPI(title="Episoon API", version="0.1.0")
tmdb = TmdbService()


@app.get("/")
async def root():
    return {"service": "Episoon API", "version": "0.1.0", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/search", response_model=list[SearchResult])
async def search(q: str):
    # Zoek films en series op via TMDB
    if not q:
        return []
    return tmdb.search(q)


@app.get("/titles/{tmdb_id}", response_model=TitleDetail)
async def get_title(tmdb_id: int, media_type: str):
    # Haal details op voor een film of serie
    if media_type not in ("movie", "tv"):
        raise HTTPException(status_code=400, detail="media_type moet 'movie' of 'tv' zijn")
    return tmdb.get_details(tmdb_id, media_type)
