# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['TimeSeries', 'TimeseriesModel', 'NaiveForecast', 'TrendForecast', 'ETSModel', 'ForecastingTask']

# Cell

from nbdev.showdoc import *
import pandas as pd
import seaborn as sns
from abc import ABC, abstractmethod
from sktime.forecasting.ets import AutoETS
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.trend import TrendForecaster

# Cell

class TimeSeries():

    """

    The Timeseries objects has 4 attributes:

    - data (DataFrame) : the DataFrame of the Timeseries
    - id_column (String) : Name of the Column from the DataFrame where the Unique IDs are located
    - date_column (String) : Name of the Colum where the Date is located
    - value_column (String) : Name of the Column where the values to messure are located

    """

    def __init__(self, data: pd.DataFrame, date_column: str, id_col: str, value_col: str):

        self.data = data
        self.date_col = date_column
        self.id_col = id_col
        self.value_col = value_col

    def __repr__(self):
        return self.data.head().to_string()

    def __str__(self):
        return self.data.head().to_string()

    def get_no_series(self):

        # Gets the number of unique series inside the dataset

        return self.data[self.id_col].unique().size

    #Adding function to get the ID from the DataFrame

    def get_id(self):

        return self.data.iloc[0][self.id_col]

    #Adding function to get the Datum Values from the DataFrame

    def get_datum(self):

        return self.data[self.date_col].unique()

    def plot_subset(self, col_wrap):

        # Plots some timeseries

        g = sns.FacetGrid(self.data, col=self.id_col, col_wrap=col_wrap)
        g.map(sns.lineplot, self.date_col, self.value_col)

# Cell
class TimeseriesModel(ABC):

    @abstractmethod
    def prepare_data(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def refit(self):
        pass


# Cell
class NaiveForecast(TimeseriesModel):

    def __init__(self, forecasting_task):
        self.forecasting_task = forecasting_task
        self.fh = forecasting_task.forecast_horizon

    @property
    def method_name(self):
        return "naive_forecaster"

    def prepare_data(self):

        value_col = self.forecasting_task.value_col
        return self.forecasting_task.train.data[value_col].reset_index(drop=True).squeeze()

    def fit(self):

        input_data = self.prepare_data()
        self.model = NaiveForecaster(strategy='last')
        self.model.fit(input_data)

    def predict(self, mode = "val"):

        if mode == "val":
            predict_data = self.forecasting_task.validation.data
            forecasts = self.model.predict(predict_data.index)
            return(forecasts)


    def refit(self):
        pass


# Cell
class TrendForecast(TimeseriesModel):

    def __init__(self, forecasting_task):
        self.forecasting_task = forecasting_task
        self.fh = forecasting_task.forecast_horizon

    @property
    def method_name(self):
        return "Trend_forecaster"

    def prepare_data(self):

        value_col = self.forecasting_task.value_col
        return self.forecasting_task.train.data[value_col].reset_index(drop=True).squeeze()

    def fit(self):

        input_data = self.prepare_data()
        self.model = TrendForecaster()
        self.model.fit(input_data)

    def predict(self, mode = "val"):

        if mode == "val":
            predict_data = self.forecasting_task.validation.data
            forecasts = self.model.predict(predict_data.index)
            return(forecasts)


    def refit(self):
        pass


# Cell

class ETSModel(TimeseriesModel):

    def __init__(self, forecasting_task):
        self.forecasting_task = forecasting_task
        self.fh = forecasting_task.forecast_horizon

    @property
    def method_name(self):
        return "auto_ets"


    def prepare_data(self):

        value_col = self.forecasting_task.value_col
        return self.forecasting_task.train.data[value_col].reset_index(drop=True).squeeze()


    def fit(self):

        input_data = self.prepare_data()
        self.model = AutoETS()
        self.model.fit(input_data)


    def predict(self, mode = "val"):

        if mode == "val":
            predict_data = self.forecasting_task.validation.data
            forecasts = self.model.predict(predict_data.index)
            return(forecasts)


    def refit(self):
        pass


# Cell
class ForecastingTask():

    def __init__(self, train: TimeSeries, out_of_sample: TimeSeries, validation: TimeSeries, forecast_horizon):

        self.train= train
        self.out_of_sample= out_of_sample
        self.validation = validation
        self.forecast_horizon = forecast_horizon

        self.value_col = self.train.value_col

        # attributes for tracking if forecasts were generated
        self.forecasted_val = False
        self.forecasted_oos = False
