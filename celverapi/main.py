# AUTOGENERATED! DO NOT EDIT! File to edit: 01_main.ipynb (unless otherwise specified).

__all__ = ['df', 'id_column', 'date_col', 'date_to_split', 'value_col', 'forecast_horizon', 'unique_dataframe_values',
           'list_of_df', 'split_into_train_test_dataframe', 'converting_dataframes_into_objects', 'ets_func',
           'naive_func', 'trend_func', 'main']

# Cell

from .core import *
import pandas as pd
import concurrent.futures

# Cell

# ---- Loading DataFrame

df = pd.read_parquet('C:/Users/kevinkeipert/Desktop/Data/example.parquet')

# ---- Project Variables

id_column = "store_nbr"         #Name of the Column where the Product IDs are located.
                                #This will split the DataFrame into smaller DataFrames from every single unique value in the column.

date_col = "date"               #Name of the Colum where the Date is located.

date_to_split = "2017-08-01"    #YYYY-MM-DD from where we want to split the DataFrames into Training and Test sets.
                                #In this example, the Train set will be every day until 2017-08-01. And the Test set from 2017-08-01 (inclusive), until the end of the DataFrame.

value_col = "sales"             #Name of the Column where the values to messure are located.
                                #In this example is the sales Column that contains the amount of money per day.

forecast_horizon = 15           #Amount of steps to forecast

# Cell

def unique_dataframe_values(id_column: str):

    """"
    This Function returns a List of DataFrames from every unique Value in the ID Column.
    Parameter:

    -   id_column (String) : Name of the Column from the DataFrame where the Unique IDs are located.
                             This will split the DataFrame into smaller DataFrames from every single unique value in the column.
    """

    list_of_df = []

    array_uvalues = df[id_column].unique()

    for value in array_uvalues:

        df_value = df[df[id_column] == value]
        list_of_df.append(df_value)

    return list_of_df

list_of_df = unique_dataframe_values(id_column)

# Cell
# ---- Splitting the DataFrames into Train and Test  ----
# ---- The DataFrames are saved in 2 Differents Lists, one for TRAIN DF and other for TEST DF ----

def split_into_train_test_dataframe(date_col: str, date_to_split: str):

    list_df_train = []
    list_df_val = []

    for df in list_of_df:

        df_train = df[df[date_col] < date_to_split]
        df_val = df[df[date_col] >= date_to_split]

        list_df_train.append(df_train)
        list_df_val.append(df_val)

    return list_df_train, list_df_val

list_df_train, list_df_val = split_into_train_test_dataframe(date_col, date_to_split)


# Cell
# ---- Creating TimeSeries Object from the respective DataFrames ---------
# ---- We append the objects again in two different lists ----------------


def converting_dataframes_into_objects(date_col, id_col, value_col, forecast_horizon: int):

    trained_ts = []
    valed_ts = []

    for df in list_df_train:

        ts_train = TimeSeries(df, date_col, id_col, value_col)
        trained_ts.append(ts_train)

    for df in list_df_val:

        ts_val = TimeSeries(df, date_col, id_col, value_col)
        valed_ts.append(ts_val)

    dict_of_forecasting_tasks = {}

    for i in range(len(trained_ts)):

        ft = ForecastingTask(train=trained_ts[i], out_of_sample=None, validation=valed_ts[i], forecast_horizon= forecast_horizon)
        dict_of_forecasting_tasks[trained_ts[i].get_id()] = ft


    return trained_ts, valed_ts, dict_of_forecasting_tasks

trained_ts, valed_ts, dict_of_forecasting_tasks = converting_dataframes_into_objects(date_col, id_column, value_col, forecast_horizon)


# Cell
# ---- Functions from the respective Models ---------

def ets_func(ft: ForecastingTask):

    ets = ETSModel(ft)
    ets.fit()
    prediction = ets.predict()
    id = ft.train.get_id()
    datum = ft.validation.get_datum()

    final_dataframe = prediction.to_frame(name='Qty')
    final_dataframe['ID'] = id
    final_dataframe['Datum'] = datum
    final_dataframe['Model'] = 'ETS-Model'

    return final_dataframe

def naive_func(ft: ForecastingTask):

    naive = NaiveForecast(ft)
    naive.fit()
    prediction = naive.predict()
    id = ft.train.get_id()
    datum = ft.validation.get_datum()

    final_dataframe = prediction.to_frame(name='Qty')
    final_dataframe['ID'] = id
    final_dataframe['Datum'] = datum
    final_dataframe['Model'] = 'Naive Model'

    return final_dataframe

def trend_func(ft: ForecastingTask):

    theta = TrendForecast(ft)
    theta.fit()
    prediction = theta.predict()
    id = ft.train.get_id()
    datum = ft.validation.get_datum()

    final_dataframe = prediction.to_frame(name='Qty')
    final_dataframe['ID'] = id
    final_dataframe['Datum'] = datum
    final_dataframe['Model'] = 'Trend Model'

    return final_dataframe


# Cell
def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:

        # Run, for example various TimeSeries simultainly for Arima Model
        ets_prediction = executor.map(ets_func, dict_of_forecasting_tasks.values())
        naive_prediction = executor.map(naive_func, dict_of_forecasting_tasks.values())
        theta_prediction = executor.map(trend_func, dict_of_forecasting_tasks.values())

        # List with all the Forecasted Objects
        final_results_ets = []
        final_results_naive = []
        final_results_trend = []

        #Appending the objects to the list
        for result in ets_prediction:
            final_results_ets.append(result)

        for result in naive_prediction:
            final_results_naive.append(result)

        for result in theta_prediction:
            final_results_trend.append(result)

        result_ets = pd.concat(final_results_ets)
        result_naive = pd.concat(final_results_naive)
        result_trend = pd.concat(final_results_trend)

        print(result_ets)
        print(result_naive)
        print(result_trend)

if __name__ == '__main__':
     main()
