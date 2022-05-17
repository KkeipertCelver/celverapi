# AUTOGENERATED! DO NOT EDIT! File to edit: 10_weather.ipynb (unless otherwise specified).

__all__ = ['ApiKey', 'get_forecast']

# Cell

from nbdev.showdoc import *
import pandas as pd
import requests

# Cell
ApiKey='37QNHAHY6SEXQ4N3R8MMQYZ3T'


# Cell

"get_forecast returns a DataFrame from a given Forecast"

def get_forecast(city: str, start_date: str, end_date: str):

    """
    The function takes 4 Parameters:

    - City(String) : The name of the city you want to Forecast
    - Start_date(String) : The starting date YYYY-MM-DD
    - End_date(String) : The ending date YYYY-MM-DD

    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&include=current&key={ApiKey}&contentType=json"
    response = requests.get(url).json()

    # ---- Converts the JSON response into a Pandas DataFrame
    # ---- Every Day is line in the Pandas DataFrame

    df = pd.json_normalize(response['days'])

    return df


