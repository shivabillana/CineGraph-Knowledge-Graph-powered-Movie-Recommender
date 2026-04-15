from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommender import (
    recommend_by_genre,
    recommend_by_director,
    recommend_by_company,
    recommend_combined
)
from models import RecommendationResponse, CombinedRecommendationResponse

app = FastAPI(
    title="Movie Recommender API",
    description="Knowledge Graph based movie recommendations using Neo4j",
    version="1.0.0"
)

# Needed so Streamlit can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Movie Recommender API is running"}

@app.get("/recommend/genre", response_model=RecommendationResponse)
def genre_recommendations(movie: str, limit: int = 10):
    results = recommend_by_genre(movie, limit)
    if not results:
        raise HTTPException(status_code=404, detail=f"Movie '{movie}' not found")
    return {"movie": movie, "recommendations": results}

@app.get("/recommend/director", response_model=RecommendationResponse)
def director_recommendations(movie: str, limit: int = 10):
    results = recommend_by_director(movie, limit)
    if not results:
        raise HTTPException(status_code=404, detail=f"Movie '{movie}' not found")
    return {"movie": movie, "recommendations": results}

@app.get("/recommend/company", response_model=RecommendationResponse)
def company_recommendations(movie: str, limit: int = 10):
    results = recommend_by_company(movie, limit)
    if not results:
        raise HTTPException(status_code=404, detail=f"Movie '{movie}' not found")
    return {"movie": movie, "recommendations": results}

@app.get("/recommend", response_model=CombinedRecommendationResponse)
def combined_recommendations(movie: str, limit: int = 10):
    results = recommend_combined(movie, limit)
    if not results:
        raise HTTPException(status_code=404, detail=f"Movie '{movie}' not found")
    return {"movie": movie, "recommendations": results}

@app.get("/movies/search")
def search_movies(q: str):
    from database import get_driver
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE toLower(m.name) CONTAINS toLower($q)
            RETURN m.name AS title
            ORDER BY m.name LIMIT 10
        """, q=q)
        return {"results": [r["title"] for r in result]}