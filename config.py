class Config:
    FILE_PATH = "data/imdb_top_1000.csv"
    ENCODING = "utf-8"

    REQUIRED_COLUMNS = [
        "Series_Title",
        "Genre",
        "Director",
        "IMDB_Rating"
    ]

    DATE_COLUMNS = []

    NUMERIC_COLUMNS = [
        "IMDB_Rating",
        "Meta_score",
        "No_of_Votes",
        "Runtime"
    ]

    MULTI_VALUE_COLUMNS = [
        "Genre",
        "Director",
        "Star1",
        "Star2",
        "Star3",
        "Star4"
    ]

    MISSING_VALUE_STRATEGY = "fill"
    FILL_VALUE = "Unknown"
