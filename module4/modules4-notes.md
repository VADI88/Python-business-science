

## 1. Cumulative Aggregate

**Definition**: Cumulative aggregates compute a running total or summary statistic over time. Common operations include cumulative sum, cumulative max, cumulative min, and cumulative product.

- **Functions**: `.cumsum()`, `.cummax()`, `.cummin()`, `.cumprod()`

**Example**:
```python
import pandas as pd

data = pd.Series([10, 20, 30, 40])
data.cumsum()
# Output: 10, 30, 60, 100
```
##  2. Rolling Aggregate

Definition: Rolling aggregates apply a function (e.g., mean, sum) over a sliding window of fixed size across a time series.

Functions: .rolling(window).mean(), .rolling(window).sum(), etc
``` python
import pandas as pd
s = pd.Series([1, 2, 3, 4, 5])
s.rolling(window=3).mean()
# Output: NaN, NaN, 2.0, 3.0, 4.0
```


## 3. Timestamp to Period

Definition: Converts a timestamp (point in time) to a period (span of time, like a month or quarter).

Function: .to_period(freq)
Example:
```python 
ts = pd.Timestamp('2023-07-01')
period = ts.to_period('M')
# Output: Period('2023-07', 'M')
Batch Example with Series:

dates = pd.date_range('2023-01-01', periods=3, freq='D')
pd.Series(dates).dt.to_period('M')
# Output: PeriodIndex(['2023-01', '2023-01', '2023-01'], dtype='period[M]')

```

4. Lags and Leads

Definition: Lag shifts data forward (past), lead shifts data backward (future).

Function: .shift(periods)
Example:
```python
s = pd.Series([10, 20, 30, 40])

# Lag (previous value)
s.shift(1)
# Output: NaN, 10, 20, 30

# Lead (next value)
s.shift(-1)
# Output: 20, 30, 40, NaN

```
5. Time Adding / Subtracting

Definition: Adding or subtracting timedeltas to timestamps or datetime columns.

Tools: pd.Timedelta, pd.DateOffset, arithmetic operations
Examples:

Add days:
```python

ts = pd.Timestamp('2023-01-01')
ts + pd.Timedelta(days=5)
# Output: Timestamp('2023-01-06')
Subtract months:

ts - pd.DateOffset(months=1)
# Output: Timestamp('2022-12-01')

dates = pd.date_range('2023-01-01', periods=3)
dates + pd.Timedelta(weeks=1)
# Output: Dates shifted forward by 7 days

```
