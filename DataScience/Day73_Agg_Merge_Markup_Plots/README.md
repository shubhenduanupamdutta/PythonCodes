# Learned

## How to combine a Notebook with HTML markup
- adding image using <img src="linkToImage">
- lists using <ul> <li> 1 </li> <li> 2 </li> </ul>

## Some new methods useful in data exploration
- nunique()  Counts number of unique objects in data
- value_counts() Finds the number of unique items in categories
## Apply python list slicing techniques to Pandas DataFrames
- df[:n] to slice dataframe by rows

## How to aggregate data using the .agg() function
- agg({"colName": pd.Series.fun})
 
## How to create scatter plots, bar charts and line charts with two axis in Matplotlib
- plt.scatter()
- plt.bar()
- ax1 = plt.gca(); ax2 = ax1.twinx()
- ax1.set_xlabel()
- ax1.set_ylabel()

## Understand Database schemas that are organised by primary and foreign keys

## How to merge DataFrames that share a common key
- merge(left_df, right_df, on="columnName")
