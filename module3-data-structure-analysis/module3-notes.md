# 1.0 Data structure:

How Python Works: Objects

Everything is objects and have classes 
Class has either attributes and methods 

```{python}
df = pd.read_csv('data.csv')

type(df) # <class 'pandas.core.frame.DataFrame'>

# Provides list of class that were inherted by this object 
type(df).mro() # [<class 'pandas.core.frame.DataFrame'>, <class 'pandas.core.generic.NDFrame'>, <class 'pandas.core.base.PandasObject'>, <class 'pandas.core.accessor.DirNamesMixin'>, <class 'pandas.core.indexing.IndexingMixin'>, <class 'pandas.core.arraylike.OpsMixin'>, <class 'object'>]

# attributes 
# without brackets

df.shape

df.columns 


# methods: 

df.query("col1 == 'val1'") 

```

# 2.0 Data Wrangling 
##  2.1 Column-wise selection 
1. isin

Definition: Filters rows based on whether column values are in a list.
```
import pandas as pd

df = pd.DataFrame({'fruit': ['apple', 'banana', 'orange', 'apple']})
df[df['fruit'].isin(['apple', 'orange'])]

```

2. iloc

Definition: Selects rows/columns by integer position.
```
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df.iloc[0]        # First row
df.iloc[0, 1]     # First row, second column (value 3)
```

3. nlargest / nsmallest

Definition: Return the top/bottom n rows sorted by a column.
```
df = pd.DataFrame({'val': [10, 50, 20, 40]})
df.nlargest(2, 'val')     # Top 2 values
df.nsmallest(2, 'val')    # Bottom 2 values

```
4. sample

Definition: Randomly samples rows from the DataFrame.
```
df.sample(n=2)        # 2 random rows
df.sample(frac=0.5)   # 50% of the data

```
5. assign

Definition: Add new columns to a DataFrame.
```
df.assign(double_val=lambda x: x['val'] * 2)

```

6. cut

Definition: Bin continuous data into discrete intervals.
```
ages = pd.Series([22, 45, 25, 65, 33])
pd.cut(ages, bins=[0, 30, 50, 100], labels=["Young", "Middle-aged", "Senior"])
```

7. groupby + agg

Definition: Group and apply aggregation functions.
```
df = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B'],
    'val': [10, 20, 30, 40]
})

df.groupby('group').agg({'val': ['mean', 'sum']})
```

8. groupby + transform

Definition: Return values aligned to the original index with group-wise calculations.
```
df['group_mean'] = df.groupby('group')['val'].transform('mean')
```

9. stack

Definition: Pivot columns into a single row-level index.
```
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df.stack()
```
10. unstack

Definition: Pivot row-level index back into columns.
```
df.stack().unstack()
```
11. rename

Definition: Rename DataFrame columns or index.
```
df.rename(columns={'val': 'value'})
```
12. pivot / pivot_table

Definition: Reshape data — similar to pivot tables in Excel.
```
df = pd.DataFrame({
    'date': ['2023', '2023', '2024'],
    'product': ['A', 'B', 'A'],
    'sales': [100, 150, 200]
})

# Pivot
df.pivot(index='date', columns='product', values='sales')

# Pivot table with aggregation
df.pivot_table(index='date', columns='product', values='sales', aggfunc='sum')
```

13. merge

Definition: Merge DataFrames based on common columns or indices (SQL-style joins).
```
df1 = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
df2 = pd.DataFrame({'id': [1, 2], 'score': [90, 85]})
pd.merge(df1, df2, on='id')
```

14. melt

Definition: Unpivot DataFrame from wide to long format.
```
df = pd.DataFrame({'id': [1], 'math': [90], 'science': [85]})
pd.melt(df, id_vars=['id'], value_vars=['math', 'science'],
        var_name='subject', value_name='score')
```
15. concat

Definition: Concatenate multiple DataFrames along rows or columns.
```
df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'A': [3, 4]})
pd.concat([df1, df2])
```
16. Splitting a column with expand

Definition: Use str.split(..., expand=True) to split a column into multiple.
```
df = pd.DataFrame({'name': ['John Smith', 'Jane Doe']})
df[['first', 'last']] = df['name'].str.split(" ", expand=True)
```


17. pipe

Definition: Functional way to chain operations on a DataFrame.
```
def add_5(df):
    df['val'] += 5
    return df

df = pd.DataFrame({'val': [1, 2, 3]})
df.pipe(add_5)
```

