# celverapi
> Library that allows the user to forecast multipletime Timeseries, parallel, using multiprocessing 


## Install

`pip install celverapi`

## How to use the Forecasting API 

In this example we are going to use a DataFrame from 4 different grocery stores. 
The idea is to Forecast various models, from every single store, simultaneously 

```python
from celverapi.core import *
from celverapi.main import *
import pandas as pd
```

```python
df = pd.read_parquet('Data/example.parquet')
#df.head(10)
```

Using the function unique_dataframe_values(), we are going to create a list of DataFrames from every unique ID value in the Main DataFrame. 
In this case, we need a DataFrame from every Store.

```python
list_of_DataFrames = unique_dataframe_values('store_nbr')
list_of_DataFrames
```




    [            date  store_nbr     family   sales  onpromotion
     0     2013-01-01          6  GROCERY I     0.0          0.0
     4     2013-01-02          6  GROCERY I  5535.0          0.0
     8     2013-01-03          6  GROCERY I  4040.0          0.0
     12    2013-01-04          6  GROCERY I  3314.0          0.0
     16    2013-01-05          6  GROCERY I  4857.0          0.0
     ...          ...        ...        ...     ...          ...
     6716  2017-08-11          6  GROCERY I  4466.0        776.0
     6720  2017-08-12          6  GROCERY I  4027.0        770.0
     6724  2017-08-13          6  GROCERY I  5481.0        817.0
     6728  2017-08-14          6  GROCERY I  4142.0        773.0
     6732  2017-08-15          6  GROCERY I  4334.0        779.0
     
     [1684 rows x 5 columns],
                 date  store_nbr     family   sales  onpromotion
     1     2013-01-01          7  GROCERY I     0.0          0.0
     5     2013-01-02          7  GROCERY I  4172.0          0.0
     9     2013-01-03          7  GROCERY I  3279.0          0.0
     13    2013-01-04          7  GROCERY I  2681.0          0.0
     17    2013-01-05          7  GROCERY I  2662.0          0.0
     ...          ...        ...        ...     ...          ...
     6717  2017-08-11          7  GROCERY I  3146.0        695.0
     6721  2017-08-12          7  GROCERY I  2851.0        723.0
     6725  2017-08-13          7  GROCERY I  2864.0        675.0
     6729  2017-08-14          7  GROCERY I  3872.0        744.0
     6733  2017-08-15          7  GROCERY I  3678.0        737.0
     
     [1684 rows x 5 columns],
                 date  store_nbr     family   sales  onpromotion
     2     2013-01-01          8  GROCERY I     0.0          0.0
     6     2013-01-02          8  GROCERY I  5277.0          0.0
     10    2013-01-03          8  GROCERY I  3783.0          0.0
     14    2013-01-04          8  GROCERY I  3481.0          0.0
     18    2013-01-05          8  GROCERY I  4857.0          0.0
     ...          ...        ...        ...     ...          ...
     6718  2017-08-11          8  GROCERY I  4318.0        801.0
     6722  2017-08-12          8  GROCERY I  4734.0        814.0
     6726  2017-08-13          8  GROCERY I  5050.0        842.0
     6730  2017-08-14          8  GROCERY I  4354.0        807.0
     6734  2017-08-15          8  GROCERY I  4035.0        786.0
     
     [1684 rows x 5 columns],
                 date  store_nbr     family     sales  onpromotion
     3     2013-01-01          9  GROCERY I     0.000          0.0
     7     2013-01-02          9  GROCERY I  7718.000          0.0
     11    2013-01-03          9  GROCERY I  4547.000          0.0
     15    2013-01-04          9  GROCERY I  3564.000          0.0
     19    2013-01-05          9  GROCERY I  5951.000          0.0
     ...          ...        ...        ...       ...          ...
     6719  2017-08-11          9  GROCERY I  5882.578        784.0
     6723  2017-08-12          9  GROCERY I  6686.109        804.0
     6727  2017-08-13          9  GROCERY I  6711.156        800.0
     6731  2017-08-14          9  GROCERY I  5860.789        773.0
     6735  2017-08-15          9  GROCERY I  6630.383        780.0
     
     [1684 rows x 5 columns]]



Once we have a list with the DataFrames that we want to work with, we are going to proceed splitting them into a Train and Test DataFrame.
In this case the Train DF is going to be from the Start Date until the 31-07-2017.

```python
list_of_trained_df, list_of_tested = split_into_train_test_dataframe(list_of_DataFrames, "date", "2017-08-01")
list_of_trained_df
```




    [            date  store_nbr     family   sales  onpromotion
     0     2013-01-01          6  GROCERY I     0.0          0.0
     4     2013-01-02          6  GROCERY I  5535.0          0.0
     8     2013-01-03          6  GROCERY I  4040.0          0.0
     12    2013-01-04          6  GROCERY I  3314.0          0.0
     16    2013-01-05          6  GROCERY I  4857.0          0.0
     ...          ...        ...        ...     ...          ...
     6656  2017-07-27          6  GROCERY I  3820.0        765.0
     6660  2017-07-28          6  GROCERY I  4602.0        807.0
     6664  2017-07-29          6  GROCERY I  6050.0        817.0
     6668  2017-07-30          6  GROCERY I  6664.0        840.0
     6672  2017-07-31          6  GROCERY I  5237.0        806.0
     
     [1669 rows x 5 columns],
                 date  store_nbr     family   sales  onpromotion
     1     2013-01-01          7  GROCERY I     0.0          0.0
     5     2013-01-02          7  GROCERY I  4172.0          0.0
     9     2013-01-03          7  GROCERY I  3279.0          0.0
     13    2013-01-04          7  GROCERY I  2681.0          0.0
     17    2013-01-05          7  GROCERY I  2662.0          0.0
     ...          ...        ...        ...     ...          ...
     6657  2017-07-27          7  GROCERY I  3552.0        682.0
     6661  2017-07-28          7  GROCERY I  3930.0        721.0
     6665  2017-07-29          7  GROCERY I  3320.0        704.0
     6669  2017-07-30          7  GROCERY I  3776.0        711.0
     6673  2017-07-31          7  GROCERY I  4401.0        754.0
     
     [1669 rows x 5 columns],
                 date  store_nbr     family   sales  onpromotion
     2     2013-01-01          8  GROCERY I     0.0          0.0
     6     2013-01-02          8  GROCERY I  5277.0          0.0
     10    2013-01-03          8  GROCERY I  3783.0          0.0
     14    2013-01-04          8  GROCERY I  3481.0          0.0
     18    2013-01-05          8  GROCERY I  4857.0          0.0
     ...          ...        ...        ...     ...          ...
     6658  2017-07-27          8  GROCERY I  3778.0        765.0
     6662  2017-07-28          8  GROCERY I  4913.0        816.0
     6666  2017-07-29          8  GROCERY I  5971.0        856.0
     6670  2017-07-30          8  GROCERY I  5962.0        850.0
     6674  2017-07-31          8  GROCERY I  4865.0        831.0
     
     [1669 rows x 5 columns],
                 date  store_nbr     family     sales  onpromotion
     3     2013-01-01          9  GROCERY I     0.000          0.0
     7     2013-01-02          9  GROCERY I  7718.000          0.0
     11    2013-01-03          9  GROCERY I  4547.000          0.0
     15    2013-01-04          9  GROCERY I  3564.000          0.0
     19    2013-01-05          9  GROCERY I  5951.000          0.0
     ...          ...        ...        ...       ...          ...
     6659  2017-07-27          9  GROCERY I  5172.547        714.0
     6663  2017-07-28          9  GROCERY I  5379.938        758.0
     6667  2017-07-29          9  GROCERY I  7861.719        832.0
     6671  2017-07-30          9  GROCERY I  8069.242        813.0
     6675  2017-07-31          9  GROCERY I  7676.711        794.0
     
     [1669 rows x 5 columns]]



After that, we will convert this DataFrames into TimeSeries objects and save them in their respective lists. 

```python
trained_timeseries, valed_timeseries = converting_dataframes_into_objects(list_of_trained_df, list_of_tested, 'date', 'store_nbr', 'sales')
trained_timeseries
```




    [          date  store_nbr     family   sales  onpromotion
     0   2013-01-01          6  GROCERY I     0.0          0.0
     4   2013-01-02          6  GROCERY I  5535.0          0.0
     8   2013-01-03          6  GROCERY I  4040.0          0.0
     12  2013-01-04          6  GROCERY I  3314.0          0.0
     16  2013-01-05          6  GROCERY I  4857.0          0.0,
               date  store_nbr     family   sales  onpromotion
     1   2013-01-01          7  GROCERY I     0.0          0.0
     5   2013-01-02          7  GROCERY I  4172.0          0.0
     9   2013-01-03          7  GROCERY I  3279.0          0.0
     13  2013-01-04          7  GROCERY I  2681.0          0.0
     17  2013-01-05          7  GROCERY I  2662.0          0.0,
               date  store_nbr     family   sales  onpromotion
     2   2013-01-01          8  GROCERY I     0.0          0.0
     6   2013-01-02          8  GROCERY I  5277.0          0.0
     10  2013-01-03          8  GROCERY I  3783.0          0.0
     14  2013-01-04          8  GROCERY I  3481.0          0.0
     18  2013-01-05          8  GROCERY I  4857.0          0.0,
               date  store_nbr     family   sales  onpromotion
     3   2013-01-01          9  GROCERY I     0.0          0.0
     7   2013-01-02          9  GROCERY I  7718.0          0.0
     11  2013-01-03          9  GROCERY I  4547.0          0.0
     15  2013-01-04          9  GROCERY I  3564.0          0.0
     19  2013-01-05          9  GROCERY I  5951.0          0.0]



The last part of the preparation, is to create a dictionary that maps the ID from the TimeSeries object with the ForecastingTask Object. 


```python
dict_of_forecasting_tasks = creating_forecasting_task_dict(trained_timeseries, valed_timeseries, forecast_horizon=15)
dict_of_forecasting_tasks
```




    {6: <celverapi.core.ForecastingTask at 0x1b36fdf2b20>,
     7: <celverapi.core.ForecastingTask at 0x1b36fdf2af0>,
     8: <celverapi.core.ForecastingTask at 0x1b36fdf2a30>,
     9: <celverapi.core.ForecastingTask at 0x1b36fdf2f70>}



To Forecast this TimeSeries, we need to call the forecast() function, where we need to pass a list of the models that we want to use and the Forecasting Task dictionary.


```python
if __name__ == "__main__":
    final_result = forecast(['ets', 'naive', 'trend'], dict_of_forecasting_tasks)

#final_result 
#Removing DF for index HTML
```

## How to use the Weather API 

```python
from celverapi.weahter import * 
```

First of all, you will need to assign your API Key from Visual Crosssing to the ApiKey variable 

```python
ApiKey='37QNHAHY6SEXQ4N3R8MMQYZ3T'
```

In order to get a DataFrame from a particular Weather Forecast, you just need to call the get_forecast() function with the required parameters and assing it to a variable.
In this particular example, we are going to get the Weather Forecast for the City of Hamburg from 17-05-2022 until 22-05-2022

```python
dataframe = get_forecast("Hamburg", "2022-05-17", "2022-05-22")
print(dataframe)
```

         datetime  datetimeEpoch  tempmax  tempmin  temp  feelslikemax  \
    0  2022-05-17     1652738400     18.3     13.3  15.3          18.3   
    1  2022-05-18     1652824800     25.3     11.0  17.8          25.3   
    2  2022-05-19     1652911200     25.2     13.1  18.5          25.2   
    3  2022-05-20     1652997600     18.6     10.0  14.0          18.6   
    4  2022-05-21     1653084000     16.8      9.1  12.7          16.8   
    5  2022-05-22     1653170400     19.8      8.1  13.8          19.8   
    
       feelslikemin  feelslike   dew  humidity  ...   sunrise  sunriseEpoch  \
    0          13.3       15.3  13.3      88.1  ...  05:16:23    1652757383   
    1          11.0       17.8  13.8      79.0  ...  05:14:51    1652843691   
    2          13.1       18.5  15.9      86.2  ...  05:13:20    1652930000   
    3           9.4       13.9  12.1      88.8  ...  05:11:52    1653016312   
    4           6.8       12.2  10.1      85.1  ...  05:10:27    1653102627   
    5           7.2       13.5   9.0      75.5  ...  05:09:04    1653188944   
    
         sunset sunsetEpoch  moonphase              conditions  \
    0  21:17:36  1652815056       0.52          Rain, Overcast   
    1  21:19:12  1652901552       0.54  Rain, Partially cloudy   
    2  21:20:47  1652988047       0.58          Rain, Overcast   
    3  21:22:21  1653074541       0.63        Partially cloudy   
    4  21:23:53  1653161033       0.68  Rain, Partially cloudy   
    5  21:25:24  1653247524       0.74        Partially cloudy   
    
                                             description               icon  \
    0  Cloudy skies throughout the day with a chance ...               rain   
    1  Partly cloudy throughout the day with storms p...               rain   
    2  Cloudy skies throughout the day with storms po...               rain   
    3                  Partly cloudy throughout the day.  partly-cloudy-day   
    4  Partly cloudy throughout the day with rain in ...               rain   
    5                  Partly cloudy throughout the day.  partly-cloudy-day   
    
                               stations  source  
    0  [EDHI, EDDH, EDHL, E9645, C7997]    comb  
    1                              None    fcst  
    2                              None    fcst  
    3                              None    fcst  
    4                              None    fcst  
    5                              None    fcst  
    
    [6 rows x 36 columns]
    
