import pandas as pd

class DataLoader:

    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.file_path, encoding=self.encoding)
            return df
        except Exception as e:
            raise Exception(f"Error loading dataset: {e}")
