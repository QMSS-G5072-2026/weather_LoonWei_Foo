import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather import (
    celsius_to_fahrenheit,
    clean_readings,
    heat_alert,
    run_pipeline,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


# TODO: add @pytest.mark.parametrize with at least 5 (celsius, expected) cases,
# including absolute zero itself.
@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0), 
        (100, 212.0),
        (-40, -40.0),
        (37, 98.6),
        (-273.15, -459.67),
    ],
)

def test_celsius_to_fahrenheit(celsius, expected):
    """TODO: One assertion (using pytest.approx) that works for every case."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected) #Comparing the expected with the calculated


# TODO: add @pytest.mark.parametrize with at least 4 (bad_input, expected_error) cases.
@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("25", TypeError),
        (None, TypeError),
        (True, TypeError),
        (-273.16, ValueError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """TODO: One pytest.raises block that works for every case."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """
    TODO: Use the Arrange / Act / Assert pattern to test a list that contains one NaN.
    Check all four keys of the returned dictionary.
    """
    #Arrange a random list with one NaN
    temps = [20.0, 30.0, float("nan"), 10.0]
    #Act - using summary
    summary = summarize_temperatures(temps)
    #Assert - compare it with the calculated "right" answer
    assert summary["mean"] == pytest.approx(20.0)
    assert summary["min"] == pytest.approx(10.0)
    assert summary["max"] == pytest.approx(30.0)
    assert summary["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """TODO: Return the station DataFrame given in Part 2 of hw06.md."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """TODO: Check the fixture has the columns, number of rows, and missing values you expect."""
    #1.Uses the fixture to check the columns
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    #2.Check no. of rows
    assert len(raw_readings) == 5
    #3.Check no. of missing values
    assert raw_readings["temp_c"].isna().sum() == 1
    

# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """TODO: Build the expected DataFrame by hand and compare with assert_frame_equal."""
    #Pass raw readings fixture to the clean_readings
    result = clean_readings(raw_readings)
    #List of changes to construct DF by hand:
    #1.NaN row (JFK, 2026-07-01) is dropped.
    #2.Row 999.0 (CPK, 2026-07-02) is also dropped
    #3.Add temp_f to convert to farenheit: (25.0 -> 77.0, 30.0 -> 86.0, 28.0 -> 82.4)
    #4.Sort by station, then data, and the reset the index
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    #Assert
    assert_frame_equal(result, expected)



def test_version_is_defined():
    assert isinstance(weather_lf2927.__version__, str)
