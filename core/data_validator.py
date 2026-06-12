class DataValidator:

    def __init__(self, df):
        self.df = df

    def validate_required_columns(self, required_columns):
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True
