
# Modules 1 - Jumpstart

## Introduction:

This modules provides introduction to all the functions and methods that might be helpful for data analysis. 
The workflow of any data project starts: 
- Importing the raw data using `pandas`
- Examining the data 
- joining the multi-data into single source (if necessary)
- data wrangling
- data visualisation 
- 
### Importing the data
#### Libraries
For best practices, Import only methods that are required for analysis.
Exception : `numpy,pandas,matplotlib` are import along with **alias**


```python
# Good  
import pandas as pd 
import numpy as np 

from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_line) 

# bad 
from plotnine import *

```
#### Path 
`path` library provides nicer way to deal with folder path and files path

```python
from path import Path 

data_folder_path = Path('path/to/data')

print(data_folder_path / 'file_name')

```

#### Janitor packages

`Janitor` library provides many methods for quick data wrangling.
 
`clean_names` on **dataframe** will clean the columns names and standarized the columns to snakes_cases.

__More methods need to check later__


```python
import pandas as pd
import janitor
df = pd.DataFrame(
    {
        "Aloha": range(3),
        "Bell Chart": range(3),
        "Animals@#$%^": range(3)
    }
)

df.clean_names(remove_special=True)
```
``` 
# output 
   aloha  bell_chart  animals
0      0           0        0
1      1           1        1
2      2           2        2

```

`deconcatenate_column` split a single column into multiple column

```python
import pandas as pd 
import janitor

df = pd.DataFrame({"m": ["1-x", "2-y", "3-z"]})

df.deconcatenate_column("m", sep="-", autoname="col")

```

``` 
# output 
  m col1 col2
0  1-x    1    x
1  2-y    2    y
2  3-z    3    z
```

#### Copy vs reference  - Pandas 

| Feature                | **Copy**                                                                                     | **Reference**                                       |
| ---------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Definition**         | Creates a **new object** with its **own data**                                               | Points to the **same object/data**                  |
| **Effect on Original** | Changes to the copy **don’t affect** the original                                            | Changes to the reference **do affect** the original |
| **Memory**             | Requires **new memory**                                                                      | Shares the **same memory**                          |
| **Syntax Example**     | `df_copy = df.copy()`                                                                        | `df_ref = df` or `df_ref = df['col']`               |
| **Use Case**           | When you need to modify data safely without side effects                                     | When you want to view or work on the same data      |
| **Common Pitfall**     | Copying a slice without `.copy()` may still behave like a reference (SettingWithCopyWarning) | You might unintentionally modify the original data  |


Use .copy() when you want to avoid modifying the original data.
