import pandas as pd

class DataTransformer:

    def __init__(self, df):
        self.df = df

    def convert_dates(self, columns):
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
        return self

    def convert_numeric(self, columns):
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
        return self

    def split_multivalue_column(self, column, separator=","):
        if column in self.df.columns:
            self.df[column] = self.df[column].apply(
                lambda x: [i.strip() for i in str(x).split(separator)]
                if pd.notnull(x) else []
            )
        return self

    def split_multiple_columns(self, columns):
        for col in columns:
            self.split_multivalue_column(col)
        return self

    def get_data(self):
        return self.df
