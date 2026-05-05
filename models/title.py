from pydantic import BaseModel


class SearchResult(BaseModel):
    tmdb_id: int
    title: str
    type: str  # 'movie' of 'tv'
    year: str | None
    poster_url: str | None
    rating: float


class TitleDetail(SearchResult):
    description: str | None
    genres: list[str]
