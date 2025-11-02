from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from file_ingestor.base_loader import BaseLoader
from file_ingestor.logger import logger


class JsonFileLoader(BaseModel, BaseLoader):
    """Loader for JSON files."""

    file_path: str = Field(..., description="Path to the JSON file to be loaded")
    encoding: str = "utf-8"

    @classmethod
    @field_validator("file_path", mode="before")
    def validate_file_path(cls, value: str) -> str:
        """Validates that the file path points to a JSON file.

        Args:
            value (str): The file path to validate.

        Raises:
            ValueError: If the file path does not end with .json.

        Returns:
            value (str): The validated file path.
        """
        if not Path(value).suffix == ".json":
            logger.error("Invalid file extension for JSON file.")
            raise ValueError("file_path must point to a JSON file")
        return value

    def load_data(self) -> pd.DataFrame:
        """Loads data from the specified JSON file.

        Raises:
            RuntimeError: Raised if the file cannot be loaded.

        Returns:
            pd.DataFrame: DataFrame containing the loaded data.
        """
        try:
            df = pd.read_json(
                self.file_path,
                encoding=self.encoding,
            )
            return df
        except Exception as e:
            logger.error("Failed to load JSON file.")
            raise RuntimeError(f"Failed to load JSON file: {e}")


if __name__ == "__main__":
    pass
