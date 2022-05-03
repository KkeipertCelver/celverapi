# celverapi
> Library that allows the user to forecast multipletime Timeseries, parallel, using multiprocessing 


## Install

`pip install celverapi`

## How to use

In this example we are going to use a DataFrame from 4 different grocery stores. 
The idea is to Forecast various models, from every single store, simultaneously 

```python
from celverapi.core import *
from celverapi.main import *
import pandas as pd
```

```python
df = pd.read_parquet('Data/example.parquet')
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>store_nbr</th>
      <th>family</th>
      <th>sales</th>
      <th>onpromotion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2013-01-01</td>
      <td>6</td>
      <td>GROCERY I</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2013-01-01</td>
      <td>7</td>
      <td>GROCERY I</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2013-01-01</td>
      <td>8</td>
      <td>GROCERY I</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2013-01-01</td>
      <td>9</td>
      <td>GROCERY I</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2013-01-02</td>
      <td>6</td>
      <td>GROCERY I</td>
      <td>5535.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2013-01-02</td>
      <td>7</td>
      <td>GROCERY I</td>
      <td>4172.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2013-01-02</td>
      <td>8</td>
      <td>GROCERY I</td>
      <td>5277.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2013-01-02</td>
      <td>9</td>
      <td>GROCERY I</td>
      <td>7718.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2013-01-03</td>
      <td>6</td>
      <td>GROCERY I</td>
      <td>4040.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2013-01-03</td>
      <td>7</td>
      <td>GROCERY I</td>
      <td>3279.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



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
trained_timeseries, valed_timeseries = converting_dataframes_into_objects('date', 'store_nbr', 'sales')
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




    {6: <celverapi.core.ForecastingTask at 0x148d64d8400>,
     7: <celverapi.core.ForecastingTask at 0x148d64d8460>,
     8: <celverapi.core.ForecastingTask at 0x148d64d8880>,
     9: <celverapi.core.ForecastingTask at 0x148d64d8790>}



To Forecast this TimeSeries, we need to call the forecast() function, where we need to pass a list of the models that we want to use and the Forecasting Task dictionary.


```python
if __name__ == "__main__":
    final_result = forecast(['ets', 'naive', 'trend'], dict_of_forecasting_tasks)

final_result
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Qty</th>
      <th>ID</th>
      <th>Date</th>
      <th>Model</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8344</th>
      <td>5234.366950</td>
      <td>6</td>
      <td>2017-08-01</td>
      <td>ETS-Model</td>
    </tr>
    <tr>
      <th>8348</th>
      <td>5234.366950</td>
      <td>6</td>
      <td>2017-08-02</td>
      <td>ETS-Model</td>
    </tr>
    <tr>
      <th>8352</th>
      <td>5234.366950</td>
      <td>6</td>
      <td>2017-08-03</td>
      <td>ETS-Model</td>
    </tr>
    <tr>
      <th>8356</th>
      <td>5234.366950</td>
      <td>6</td>
      <td>2017-08-04</td>
      <td>ETS-Model</td>
    </tr>
    <tr>
      <th>8360</th>
      <td>5234.366950</td>
      <td>6</td>
      <td>2017-08-05</td>
      <td>ETS-Model</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>8387</th>
      <td>17776.977872</td>
      <td>9</td>
      <td>2017-08-11</td>
      <td>Trend Model</td>
    </tr>
    <tr>
      <th>8391</th>
      <td>17783.141263</td>
      <td>9</td>
      <td>2017-08-12</td>
      <td>Trend Model</td>
    </tr>
    <tr>
      <th>8395</th>
      <td>17789.304655</td>
      <td>9</td>
      <td>2017-08-13</td>
      <td>Trend Model</td>
    </tr>
    <tr>
      <th>8399</th>
      <td>17795.468047</td>
      <td>9</td>
      <td>2017-08-14</td>
      <td>Trend Model</td>
    </tr>
    <tr>
      <th>8403</th>
      <td>17801.631439</td>
      <td>9</td>
      <td>2017-08-15</td>
      <td>Trend Model</td>
    </tr>
  </tbody>
</table>
<p>180 rows × 4 columns</p>
</div>


