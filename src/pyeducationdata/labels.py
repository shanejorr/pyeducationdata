"""Label mapping functionality for converting integer codes to descriptive labels.

This module provides functionality to convert integer-coded categorical variables
to pandas Categorical dtype with human-readable labels, using metadata from the API.
"""

from typing import Any, Optional

import pandas as pd

from .api import get_default_client
from .exceptions import DataProcessingError


class LabelMapper:
    """Manages retrieval and application of variable labels.

    This class queries the API's metadata endpoints to retrieve label
    definitions and applies them to DataFrames, converting integer codes
    to categorical variables with descriptive labels.
    """

    def __init__(self):
        """Initialize the label mapper."""
        self._label_cache: dict[str, dict[int, str]] = {}
        self._variable_info_cache: Optional[list[dict[str, Any]]] = None

    def get_variable_metadata(self) -> list[dict[str, Any]]:
        """Retrieve variable metadata from the API.

        Returns:
            List of variable metadata dictionaries

        Raises:
            DataProcessingError: If metadata retrieval fails
        """
        if self._variable_info_cache is not None:
            return self._variable_info_cache

        try:
            client = get_default_client()
            metadata = client.get_metadata("variables")
            self._variable_info_cache = metadata.get("results", [])
            return self._variable_info_cache
        except Exception as e:
            raise DataProcessingError(f"Failed to retrieve variable metadata: {str(e)}") from e

    def get_label_mapping(self, variable_name: str) -> Optional[dict[int, str]]:
        """Get the label mapping for a specific variable.

        Args:
            variable_name: Name of the variable to get labels for

        Returns:
            Dictionary mapping integer codes to string labels, or None if
            the variable doesn't have labels

        Raises:
            DataProcessingError: If label retrieval fails
        """
        # Check cache first
        if variable_name in self._label_cache:
            return self._label_cache[variable_name]

        # Get variable metadata
        metadata = self.get_variable_metadata()

        # Find the variable
        variable_info = None
        for var in metadata:
            if var.get("variable") == variable_name or var.get("name") == variable_name:
                variable_info = var
                break

        if not variable_info:
            # Variable not found - no labels available
            self._label_cache[variable_name] = None
            return None

        # Extract labels if available
        labels = variable_info.get("labels") or variable_info.get("value_labels")

        if not labels:
            # No labels defined for this variable
            self._label_cache[variable_name] = None
            return None

        # Convert labels to dict format
        if isinstance(labels, dict):
            # Labels already in {code: label} format
            label_mapping = {int(k): str(v) for k, v in labels.items()}
        elif isinstance(labels, list):
            # Labels in [{code: ..., label: ...}] format
            label_mapping = {}
            for item in labels:
                if isinstance(item, dict) and "code" in item and "label" in item:
                    label_mapping[int(item["code"])] = str(item["label"])
        else:
            label_mapping = None

        # Cache and return
        self._label_cache[variable_name] = label_mapping
        return label_mapping

    def apply_labels(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Apply labels to a specific column in a DataFrame.

        Args:
            df: DataFrame to modify
            column: Column name to apply labels to

        Returns:
            DataFrame with the specified column converted to Categorical

        Raises:
            DataProcessingError: If label application fails
        """
        if column not in df.columns:
            return df

        # Get label mapping for this variable
        try:
            label_mapping = self.get_label_mapping(column)
        except Exception as e:
            # If we can't get labels, just return the DataFrame unchanged
            print(f"Warning: Could not retrieve labels for '{column}': {e}")
            return df

        if not label_mapping:
            # No labels available for this variable
            return df

        try:
            # Create a copy to avoid modifying original
            df = df.copy()

            # Map integer codes to labels
            df[column] = df[column].map(label_mapping)

            # Convert to categorical
            df[column] = pd.Categorical(df[column])

            return df

        except Exception as e:
            raise DataProcessingError(
                f"Failed to apply labels to column '{column}': {str(e)}"
            ) from e

    def apply_labels_to_dataframe(
        self, df: pd.DataFrame, columns: Optional[list[str]] = None
    ) -> pd.DataFrame:
        """Apply labels to multiple columns in a DataFrame.

        Args:
            df: DataFrame to modify
            columns: List of column names to apply labels to. If None,
                    attempts to label all applicable columns.

        Returns:
            DataFrame with categorical columns labeled

        Raises:
            DataProcessingError: If label application fails
        """
        if df.empty:
            return df

        # If no columns specified, try to identify categorical columns
        if columns is None:
            columns = self._identify_categorical_columns(df)

        # Apply labels to each column
        for column in columns:
            if column in df.columns:
                df = self.apply_labels(df, column)

        return df

    def _identify_categorical_columns(self, df: pd.DataFrame) -> list[str]:
        """Identify columns that might have categorical labels.

        This uses heuristics to identify columns that are likely to be
        categorical (integer-coded with a small number of unique values).

        Args:
            df: DataFrame to analyze

        Returns:
            List of column names that are likely categorical
        """
        categorical_columns = []

        # Common categorical variable names
        common_categorical = [
            "race",
            "sex",
            "gender",
            "fips",
            "grade",
            "school_level",
            "school_type",
            "inst_level",
            "inst_control",
            "disability",
            "lep",
        ]

        for column in df.columns:
            # Check if column name suggests it's categorical
            if any(cat in column.lower() for cat in common_categorical):
                categorical_columns.append(column)
            # Check if column has integer type with few unique values
            elif pd.api.types.is_integer_dtype(df[column]):
                n_unique = df[column].nunique()
                if n_unique < 50:  # Arbitrary threshold
                    categorical_columns.append(column)

        return categorical_columns


# Module-level singleton
_default_mapper: Optional[LabelMapper] = None


def get_default_mapper() -> LabelMapper:
    """Get or create the default label mapper instance.

    Returns:
        The default LabelMapper instance
    """
    global _default_mapper
    if _default_mapper is None:
        _default_mapper = LabelMapper()
    return _default_mapper


def apply_labels_to_dataframe(
    df: pd.DataFrame, columns: Optional[list[str]] = None
) -> pd.DataFrame:
    """Convenience function to apply labels using the default mapper.

    Args:
        df: DataFrame to modify
        columns: List of column names to apply labels to

    Returns:
        DataFrame with categorical columns labeled
    """
    mapper = get_default_mapper()
    return mapper.apply_labels_to_dataframe(df, columns)
