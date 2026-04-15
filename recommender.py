from database import get_driver

driver = get_driver()

def recommend_by_genre(movie: str, limit: int = 10):
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE toLower(m.name) = toLower($movie)
            MATCH (m)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(other:Movie)
            WHERE other <> m
            RETURN other.name AS title, count(g) AS score
            ORDER BY score DESC LIMIT $limit
        """, movie=movie, limit=limit)
        return [{"title": r["title"], "score": int(r["score"])} for r in result]


def recommend_by_director(movie: str, limit: int = 10):
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE toLower(m.name) = toLower($movie)
            MATCH (m)-[:DIRECTED_BY]->(d:Director)<-[:DIRECTED_BY]-(other:Movie)
            WHERE other <> m
            RETURN other.name AS title, count(d) AS score
            ORDER BY score DESC LIMIT $limit
        """, movie=movie, limit=limit)
        return [{"title": r["title"], "score": int(r["score"])} for r in result]


def recommend_by_company(movie: str, limit: int = 10):
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE toLower(m.name) = toLower($movie)
            MATCH (m)-[:PRODUCED_BY]->(c:Company)<-[:PRODUCED_BY]-(other:Movie)
            WHERE other <> m
            RETURN other.name AS title, count(c) AS score
            ORDER BY score DESC LIMIT $limit
        """, movie=movie, limit=limit)
        return [{"title": r["title"], "score": int(r["score"])} for r in result]


def recommend_combined(movie: str, limit: int = 10):
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE toLower(m.name) = toLower($movie)

            OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(other:Movie)
            WHERE other <> m
            WITH m, other, count(DISTINCT g) AS genre_score

            OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Director)<-[:DIRECTED_BY]-(other)
            WITH m, other, genre_score, count(DISTINCT d) * 2 AS director_score

            OPTIONAL MATCH (m)-[:PRODUCED_BY]->(c:Company)<-[:PRODUCED_BY]-(other)
            WITH other, genre_score, director_score, count(DISTINCT c) AS company_score

            RETURN other.name AS title,
                   genre_score + director_score + company_score AS total_score,
                   genre_score,
                   director_score,
                   company_score
            ORDER BY total_score DESC LIMIT $limit
        """, movie=movie, limit=limit)
        return [{
            "title": r["title"],
            "total_score": int(r["total_score"]),
            "genre_score": int(r["genre_score"]),
            "director_score": int(r["director_score"]),
            "company_score": int(r["company_score"])
        } for r in result]