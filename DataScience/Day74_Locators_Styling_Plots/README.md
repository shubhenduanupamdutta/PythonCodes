# Learned

## How to make time-series data comparable by resampling & converting to same periodicity
- #### ``new_df = old_df.resample("M", on="datetimeColumn").last()`` to convert date index to month, using last day of the month values

## Fine tuning the styling of ```matplotlib``` charts by using limits, tabels, linestyles, markers, colours and the charts' resolution
- #### ``import matplotlib.pyplot as plt``
- #### ``ax1.set_xlim([lower, upper])``
- #### ``ax1.set_ylim([lower, upper])``
- #### ``plt.figure(figsize=(width_in, height_in), dpi=resolution_int)``
- #### ``plt.plot(x, y, linestyle="-", linewidth=3, label="labe_of_line")``
- 
## Using grids to help visually identify seasonality in a time-series 
- #### ``plt.grid(color="grey", .., ..)``
- 
## Finding number of missing & ```NaN``` values & how to locate ```NaN``` values in a dataframe
- #### ``df.isna().to_numpy().sum()`` to count how many NaN values are there
- #### ``df[df['colName'].isna()]`` to find if the column has NaN values, and which rows of columns have them

## How to work with locators to better style the time axis on a chart
- #### ``import matplotlib.dates as mdates``
- #### ``YearLocator()``
- #### ``MonthLocator()``
- #### ``DateFormator()``
- #### ``plt.axis.set_major_ticks()``
- #### ``plt.axis.set_minor_ticks()``

## Review the concepts learned in previous 3 days& apply them to new data-sets
