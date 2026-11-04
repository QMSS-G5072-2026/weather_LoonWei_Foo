import math
from pathlib import Path

import pandas as pd
import requests

ABSOLUTE_ZERO_C = -273.15
MIN_PLAUSIBLE_C = -90.0
MAX_PLAUSIBLE_C = 60.0


def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert a temperature from degrees Celsius to degrees Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Raises:
        TypeError: If `celsius` is not an int or a float.
        ValueError: If `celsius` is below absolute zero (-273.15 C).
    
    Examples:
        >>> from weather_lf2927 import celsius_to_fahrenheit
        >>> celsius_to_fahrenheit(100)
        212.0
        >>> celsius_to_fahrenheit(0)
        32.0
    """
    if isinstance(celsius, bool) or not isinstance(celsius, (int, float)):
        raise TypeError("celsius must be a number")
    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError("temperature cannot be below absolute zero")
    return celsius * 9 / 5 + 32


def summarize_temperatures(temps: list[float]) -> dict[str, float]:
    """
    Summarize a list of temperature readings, ignoring missing values (NaN).

    Args:
        temps: Temperature readings. Missing readings are stored as float("nan").

    Returns:
        A dictionary with the keys "mean", "min", "max", and "n_missing".

    Raises:
        ValueError: If there are no valid (non-missing) readings.

    Examples:
        >>> from weather_lf2927 import summarize_temperatures
        >>> summarize_temperatures([20.0, float("nan"), 25.0])
        {'mean': 22.5, 'min': 20.0, 'max': 25.0, 'n_missing': 1}
    """
    valid = [t for t in temps if not math.isnan(t)]
    if not valid:
        raise ValueError("no valid temperature readings")
    return {
        "mean": sum(valid) / len(valid),
        "min": min(valid),
        "max": max(valid),
        "n_missing": len(temps) - len(valid),
    }


def clean_readings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw station readings.

    Steps:
        1. Drop rows where `temp_c` is missing.
        2. Drop physically implausible readings (outside -90 C to 60 C, inclusive bounds are kept).
        3. Add a `temp_f` column with the temperature in Fahrenheit.
        4. Sort by `station`, then `date`, and reset the index.

    Args:
        df: DataFrame with the columns `station`, `date`, and `temp_c`.

    Returns:
        A new, cleaned DataFrame. The input DataFrame is not modified.

    Examples:
        >>> import pandas as pd
        >>> from weather_lf2927 import clean_readings
        >>> raw = pd.DataFrame({
        ...     "station": ["B", "A", "A", "A"],
        ...     "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-01"],
        ...     "temp_c": [20.0, None, 100.0, 15.0],
        ... })
        >>> clean_readings(raw)
          station        date  temp_c  temp_f
        0       A  2026-01-01    15.0    59.0
        1       B  2026-01-01    20.0    68.0
    """
    cleaned = df.dropna(subset=["temp_c"])
    in_range = cleaned["temp_c"].between(MIN_PLAUSIBLE_C, MAX_PLAUSIBLE_C)
    cleaned = cleaned[in_range].copy()
    cleaned["temp_f"] = cleaned["temp_c"] * 9 / 5 + 32
    return cleaned.sort_values(["station", "date"]).reset_index(drop=True)
