from config.config import Config
from config.db_config import DBConfig
from core.pipeline import DataPipeline
from database.db_connection import DBConnection
from database.schema_manager import SchemaManager
from database.imdb_loader import IMDBLoader
from database.query_executor import QueryExecutor

def main():
    # STEP 1: ETL cleaning
    pipeline = DataPipeline(Config)
    df = pipeline.run()

    # STEP 2: Connect DB
    db = DBConnection(DBConfig)
    connection = db.connect()

    # STEP 3: Create Schema
    schema = SchemaManager(connection, "sql/schema.sql")
    schema.create_schema()

    # STEP 4: Load Data
    loader = IMDBLoader(connection)
    loader.load_dataframe(df)

    # STEP 5: Run 15+ Analytical Queries
    queries = {
        "top_10_rated_movies": """
            SELECT title, imdb_rating
            FROM movies
            ORDER BY imdb_rating DESC
            LIMIT 10;
        """,
        "top_10_movies_by_votes": """
            SELECT title, votes
            FROM movies
            ORDER BY votes DESC
            LIMIT 10;
        """,
        "avg_rating_per_director": """
            SELECT d.name AS director, AVG(m.imdb_rating) AS avg_rating
            FROM movies m
            JOIN movie_director md ON m.id = md.movie_id
            JOIN directors d ON md.director_id = d.id
            GROUP BY d.name
            ORDER BY avg_rating DESC
            LIMIT 10;
        """,
        "movies_per_genre": """
            SELECT g.name AS genre, COUNT(m.id) AS movie_count
            FROM movies m
            JOIN movie_genre mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.id
            GROUP BY g.name
            ORDER BY movie_count DESC;
        """,
        "avg_runtime_per_genre": """
            SELECT g.name AS genre, AVG(m.runtime) AS avg_runtime
            FROM movies m
            JOIN movie_genre mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.id
            GROUP BY g.name
            ORDER BY avg_runtime DESC;
        """,
        "actors_top_10_by_movie_count": """
            SELECT a.name AS actor, COUNT(ma.movie_id) AS movie_count
            FROM actors a
            JOIN movie_actor ma ON a.id = ma.actor_id
            GROUP BY a.name
            ORDER BY movie_count DESC
            LIMIT 10;
        """,
        "directors_top_10_by_movie_count": """
            SELECT d.name AS director, COUNT(md.movie_id) AS movie_count
            FROM directors d
            JOIN movie_director md ON d.id = md.director_id
            GROUP BY d.name
            ORDER BY movie_count DESC
            LIMIT 10;
        """,
        "movies_per_year": """
            SELECT release_year, COUNT(*) AS total_movies
            FROM movies
            GROUP BY release_year
            ORDER BY release_year;
        """,
        "movies_rating_above_8_5": """
            SELECT title, release_year, imdb_rating
            FROM movies
            WHERE imdb_rating > 8.5
            ORDER BY imdb_rating DESC;
        """,
        "directors_with_movies_above_9": """
            SELECT d.name AS director, COUNT(m.id) AS high_rated_movies
            FROM movies m
            JOIN movie_director md ON m.id = md.movie_id
            JOIN directors d ON md.director_id = d.id
            WHERE m.imdb_rating > 9
            GROUP BY d.name
            ORDER BY high_rated_movies DESC;
        """,
        "actors_with_movies_above_8_5": """
            SELECT a.name AS actor, COUNT(ma.movie_id) AS high_rated_movies
            FROM actors a
            JOIN movie_actor ma ON a.id = ma.actor_id
            JOIN movies m ON ma.movie_id = m.id
            WHERE m.imdb_rating > 8.5
            GROUP BY a.name
            ORDER BY high_rated_movies DESC;
        """,
        "avg_rating_per_genre": """
            SELECT g.name AS genre, AVG(m.imdb_rating) AS avg_rating
            FROM movies m
            JOIN movie_genre mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.id
            GROUP BY g.name
            ORDER BY avg_rating DESC;
        """,
        "top_10_movies_per_genre": """
            SELECT g.name AS genre, m.title, m.imdb_rating
            FROM movies m
            JOIN movie_genre mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.id
            WHERE m.imdb_rating IS NOT NULL
            ORDER BY g.name, m.imdb_rating DESC
            LIMIT 10;
        """,
        "genres_top_10_by_avg_votes": """
            SELECT g.name AS genre, AVG(m.votes) AS avg_votes
            FROM movies m
            JOIN movie_genre mg ON m.id = mg.movie_id
            JOIN genres g ON mg.genre_id = g.id
            GROUP BY g.name
            ORDER BY avg_votes DESC
            LIMIT 10;
        """,
        "directors_top_10_by_avg_votes": """
            SELECT d.name AS director, AVG(m.votes) AS avg_votes
            FROM movies m
            JOIN movie_director md ON m.id = md.movie_id
            JOIN directors d ON md.director_id = d.id
            GROUP BY d.name
            ORDER BY avg_votes DESC
            LIMIT 10;
        """
    }

    executor = QueryExecutor(connection)

    # Optional insert example
    # executor.run_insert_query(
    #     "INSERT INTO movies (title, release_year, imdb_rating) VALUES (%s, %s, %s)",
    #     ("New Movie Example", 2026, 8.7)
    # )

    results = executor.run_multiple_queries(queries)
    executor.save_results(results)

    # Close DB
    db.close()
    print("All 15+ analytical queries executed successfully!")

if __name__ == "__main__":
    main()
