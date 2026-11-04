# read version from installed package
from importlib.metadata import version
__version__ = version("weather_lf2927")

#Import the three functions from the other file here
from weather_lf2927.weather_lf2927 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)
