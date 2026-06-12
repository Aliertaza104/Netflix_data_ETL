CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_year INT,
    imdb_rating FLOAT,
    meta_score FLOAT,
    votes BIGINT,
    runtime INT
);

CREATE TABLE IF NOT EXISTS directors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS movie_director (
    movie_id INT REFERENCES movies(id),
    director_id INT REFERENCES directors(id),
    PRIMARY KEY (movie_id, director_id)
);

CREATE TABLE IF NOT EXISTS movie_actor (
    movie_id INT REFERENCES movies(id),
    actor_id INT REFERENCES actors(id),
    PRIMARY KEY (movie_id, actor_id)
);

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INT REFERENCES movies(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);
