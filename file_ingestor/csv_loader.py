import warnings

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from file_ingestor.base_loader import BaseLoader
from file_ingestor.logger import logger

warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)


class CsvFileLoader(BaseModel, BaseLoader):
    """AI is creating summary for CsvFileLoader."""

    file_path: str = Field(..., description="Path to the CSV file to be loaded")
    header: bool = False
    delimiter: str = ","
    encoding: str = "utf-8"

    @classmethod
    @field_validator("file_path", mode="before")
    def validate_file_path(cls, value):
        """Validates that the file path points to an CSV file.

        Args:
            value (str): The file path to validate.

        Raises:
            ValueError: If the file path does not end with .xlsx.

        Returns:
            value (str): The validated file path.
        """
        if not value.endswith(".csv"):
            logger.error("Invalid file extension for CSV file.")
            raise ValueError("file_path must point to a CSV file")
        return value

    def load_data(self) -> pd.DataFrame:
        """Loads data from the specified CSV file.

        Raises:
            RuntimeError: Raised if the file cannot be loaded.

        Returns:
            pd.DataFrame: DataFrame containing the loaded data.
        """
        try:
            df = pd.read_csv(
                self.file_path,
                header=0 if self.header else None,
                delimiter=self.delimiter,
                encoding=self.encoding,
            )
            return df
        except Exception as e:
            logger.error("Failed to load CSV file.")
            raise RuntimeError(f"Failed to load CSV file: {e}")


if __name__ == "__main__":
    pass
