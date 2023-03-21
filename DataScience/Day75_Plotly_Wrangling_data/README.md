# Learned

## How to quickly remove duplicates
- #### ``df.sample(n)`` to get randomly selected n rows from the DataFrame 
- #### ``df.drop(["ColName"], axis=1)`` to remove one or many columns
- #### ``df.duplicated()`` Returns True for rows which are duplicated
- #### ``df[df.duplicated()]`` To get duplicated rows
- #### ``df.drop_duplicated(["colName1", "colName2"])`` Remove duplicated rows by comparing given columns

## how to remove unwanted symbols & convert data into a numeric format
- #### ``df.colName = df.colName.astype(str).str.replace("$", "")`` removing (by replacing with nothing) a character from object type column using ``astype(str)`` to convert to string and then ``str.replace()`` to replace.
- #### ``df.colName = pd.to_numeric(df.colName)`` to convert to numeric type from string type for a cleaned column

## How to wrangle columns containing nested data with pandas
- #### ``split(";")`` split a column string by a character , here ;
- #### ``stack()`` stack new values created on the same column
- #### ``stacked_genre = df.Genres.str.split(";", expand=True).stack()`` splits Genre data where ; is used, and adds new values and old values to stacked_genre

## How to make compelling data visualizations with the plotly library
- #### ``import plotly.express as px``
- #### ``import plotly.graph_objects as go``

## Create vertical, horizontal and grouped bar charts
- #### ``px.bar(df, x="colNameX", y="ColNameY", color="colNameZ", ..)`` use option `orientation` to make horizontal or vertical
- #### ``go`` can also be used to make grouped bar charts.

## create pie & donut charts for categorical data
- #### ``px.pie(df, x="colNameX", y="colNameY")`` use option `hole` to make the chart a donut one

## Using colorscales to make beautiful scatter plots
- #### ``px.scatter(df, x="colNameX", y=colNameY", color="colorCol", size="sizeCol")``
- #### ``px.box()``
