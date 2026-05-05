import os
import httpx
from models.title import SearchResult, TitleDetail

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


class TmdbService:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")

    def _poster_url(self, poster_path: str | None) -> str | None:
        # Bouw de volledige poster URL op als er een pad beschikbaar is
        if poster_path:
            return f"{TMDB_IMAGE_BASE}{poster_path}"
        return None

    def search(self, query: str) -> list[SearchResult]:
        # Zoek films én series tegelijk via de TMDB multi-search endpoint
        with httpx.Client() as client:
            response = client.get(
                f"{TMDB_BASE_URL}/search/multi",
                params={"api_key": self.api_key, "query": query, "language": "nl-NL"},
            )
            response.raise_for_status()
            data = response.json()

        resultaten = []
        for item in data.get("results", []):
            # Filter personen eruit — we willen alleen films en series
            media_type = item.get("media_type")
            if media_type not in ("movie", "tv"):
                continue

            title = item.get("title") or item.get("name")
            date = item.get("release_date") or item.get("first_air_date")
            year = date[:4] if date else None

            resultaten.append(
                SearchResult(
                    tmdb_id=item["id"],
                    title=title,
                    type=media_type,
                    year=year,
                    poster_url=self._poster_url(item.get("poster_path")),
                    rating=item.get("vote_average", 0.0),
                )
            )

        return resultaten

    def get_details(self, tmdb_id: int, media_type: str) -> TitleDetail:
        # Haal gedetailleerde informatie op voor een specifieke film of serie
        with httpx.Client() as client:
            response = client.get(
                f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}",
                params={"api_key": self.api_key, "language": "nl-NL"},
            )
            response.raise_for_status()
            item = response.json()

        title = item.get("title") or item.get("name")
        date = item.get("release_date") or item.get("first_air_date")
        year = date[:4] if date else None
        genres = [g["name"] for g in item.get("genres", [])]

        return TitleDetail(
            tmdb_id=item["id"],
            title=title,
            type=media_type,
            year=year,
            poster_url=self._poster_url(item.get("poster_path")),
            rating=item.get("vote_average", 0.0),
            description=item.get("overview"),
            genres=genres,
        )
