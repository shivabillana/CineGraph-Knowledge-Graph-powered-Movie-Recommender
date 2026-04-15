from pydantic import BaseModel
from typing import List

class MovieRecommendation(BaseModel):
    title : str
    score : int

class CombinedRecommendation(BaseModel):
    title : str
    total_score : int
    genre_score : int
    director_score : int
    company_score : int

class RecommendationResponse(BaseModel):
    movie : str
    recommendations : List[MovieRecommendation]

class CombinedRecommendationResponse(BaseModel):
    movie : str
    recommendations : List[CombinedRecommendation]