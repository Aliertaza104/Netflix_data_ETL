class IMDBLoader:

    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    def get_or_create(self, table, name_col, name):
        """
        Checks if a name exists in a table, returns id.
        Otherwise, inserts and returns new id.
        """
        self.cursor.execute(
            f"SELECT id FROM {table} WHERE {name_col}=%s", (name,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute(
                f"INSERT INTO {table} ({name_col}) VALUES (%s) RETURNING id", (name,)
            )
            self.conn.commit()
            return self.cursor.fetchone()[0]

    def insert_movie(self, row):
        self.cursor.execute("""
            INSERT INTO movies (title, release_year, imdb_rating, meta_score, votes, runtime)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            row.get("Series_Title"),
            row.get("Released_Year"),
            row.get("IMDB_Rating"),
            row.get("Meta_score"),
            row.get("No_of_Votes"),
            row.get("Runtime")
        ))
        return self.cursor.fetchone()[0]

    def insert_junction(self, movie_id, column_values, table_name, junction_table, column_name):
        """
        Generic method to insert many-to-many relationships
        column_values: list of names
        table_name: directors/actors/genres
        junction_table: movie_director/movie_actor/movie_genre
        column_name: name column in table_name
        """
        for val in column_values:
            val_id = self.get_or_create(table_name, column_name, val)
            self.cursor.execute(
                f"""
                INSERT INTO {junction_table} (movie_id, {table_name[:-1]}_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (movie_id, val_id)
            )

    def load_dataframe(self, df):
        """
        Load entire cleaned dataframe into DB
        """
        for _, row in df.iterrows():
            # Insert movie
            movie_id = self.insert_movie(row)

            # Directors
            directors = row.get("Director") if "Director" in row else []
            if isinstance(directors, list):
                self.insert_junction(movie_id, directors, "directors", "movie_director", "name")

            # Actors
            stars = []
            for col in ["Star1", "Star2", "Star3", "Star4"]:
                if col in row:
                    stars.extend(row[col] if isinstance(row[col], list) else [row[col]])
            stars = [s for s in stars if s]  # remove empty
            if stars:
                self.insert_junction(movie_id, stars, "actors", "movie_actor", "name")

            # Genres
            genres = row.get("Genre") if "Genre" in row else []
            if isinstance(genres, list):
                self.insert_junction(movie_id, genres, "genres", "movie_genre", "name")

        # Commit all changes at the end
        self.conn.commit()
        self.cursor.close()
