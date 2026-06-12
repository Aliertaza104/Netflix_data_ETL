from core.data_loader import DataLoader
from core.data_cleaner import DataCleaner
from core.data_transformer import DataTransformer
from core.data_validator import DataValidator


class DataPipeline:

    def __init__(self, config):
        self.config = config

    def run(self):
        # Load
        loader = DataLoader(self.config.FILE_PATH, self.config.ENCODING)
        df = loader.load()

        # Validate
        validator = DataValidator(df)
        validator.validate_required_columns(self.config.REQUIRED_COLUMNS)

        # Clean
        cleaner = DataCleaner(df)
        df = (
            cleaner
            .remove_duplicates()
            .strip_whitespace()
            .handle_missing(
                strategy=self.config.MISSING_VALUE_STRATEGY,
                fill_value=self.config.FILL_VALUE
            )
            .get_data()
        )

        # Transform
        transformer = DataTransformer(df)
        df = (
            transformer
            .convert_dates(self.config.DATE_COLUMNS)
            .convert_numeric(self.config.NUMERIC_COLUMNS)
            .split_multiple_columns(self.config.MULTI_VALUE_COLUMNS)
            .get_data()
        )

        return df
