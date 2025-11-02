import warnings
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from file_ingestor.base_loader import BaseLoader
from file_ingestor.logger import logger

warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)


class ExcelFileLoader(BaseModel, BaseLoader):
    """AI is creating summary for CsvFileLoader"""

    file_path: str = Field(..., description="Path to the Excel file to be loaded")
    header: bool = False
    engine: str = "openpyxl"
    sheet_name: str | int | None = None

    @classmethod
    @field_validator("file_path", mode="before")
    def validate_file_path(cls, value: str) -> str:
        """Validates that the file path points to an Excel file.

        Args:
            value (str): The file path to validate.

        Raises:
            ValueError: If the file path does not end with .xlsx.

        Returns:
            value (str): The validated file path.
        """
        if Path(value).suffix not in [".xlsx", ".xls"]:
            logger.error("Invalid file extension for Excel file.")
            raise ValueError("file_path must point to a xlsx file")
        return value

    def load_data(self) -> pd.DataFrame:
        """Loads data from the specified Excel file.

        Raises:
            RuntimeError: Raised if the file cannot be loaded.

        Returns:
            pd.DataFrame: DataFrame containing the loaded data.
        """
        try:
            df = pd.read_excel(
                self.file_path,
                header=0 if self.header else None,
                sheet_name=self.sheet_name,
            )
            return df["student_name"]  # pyright: ignore[reportReturnType]
        except Exception as e:
            logger.error("Failed to load Excel file.")
            raise RuntimeError(f"Failed to load Excel file: {e}")


if __name__ == "__main__":
    pass
