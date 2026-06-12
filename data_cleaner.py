class DataCleaner:

    def __init__(self, df):
        self.df = df

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self

    def handle_missing(self, strategy="fill", fill_value="Unknown"):
        if strategy == "fill":
            self.df = self.df.fillna(fill_value)
        elif strategy == "drop":
            self.df = self.df.dropna()
        return self

    def strip_whitespace(self):
        self.df = self.df.applymap(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        return self

    def get_data(self):
        return self.df
