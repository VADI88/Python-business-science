## Plotnine

```python
import pandas as pd
from plotnine import *
from sklearn.datasets import load_iris

# Load a sample dataset
iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = df['target'].map(dict(enumerate(iris.target_names)))
```

# 1 Scatter Plot

```python
(
        ggplot(df, aes(x='sepal length (cm)', y='sepal width (cm)', color='species')) +
        geom_point()
)

```

# 2 Line Plot

```python
df_line = pd.DataFrame({
        'day'        : range(1, 8),
        'temperature': [30, 32, 34, 33, 31, 29, 28]
})

(
        ggplot(df_line, aes(x='day', y='temperature')) +
        geom_line() +
        geom_point()
)

```

# 3 Boxplot

```python
(
        ggplot(df, aes(x='species', y='sepal length (cm)', fill='species')) +
        geom_boxplot()
)

```

# 4 Violin Plot

```python
(
        ggplot(df, aes(x='species', y='sepal length (cm)', fill='species')) +
        geom_violin()
)

```

# 5 Histogram

```python
(
        ggplot(df, aes(x='sepal length (cm)')) +
        geom_histogram(bins=20, fill='skyblue', color='black')
)
```

# 6 Density

```python
(
        ggplot(df, aes(x='sepal length (cm)', fill='species')) +
        geom_density(alpha=0.6)
)

```

# 7 Bar Plot

```python
(
        ggplot(df, aes(x='species')) +
        geom_bar(fill='steelblue')
)

```

# 8 Facet Plot

```python
(
        ggplot(df, aes(x='sepal length (cm)', y='sepal width (cm)', color='species')) +
        geom_point() +
        facet_wrap('~species')
)

```

# 9 Custom Theme

```python
(
        ggplot(df, aes(x='sepal length (cm)', y='sepal width (cm)', color='species')) +
        geom_point(size=3) +
        labs(title='Sepal Length vs Width by Species', x='Sepal Length', y='Sepal Width') +
        theme_minimal()
)

```

# 10 Statistical Smooth Plot

```python
(
        ggplot(df, aes(x='sepal length (cm)', y='sepal width (cm)', color='species')) +
        geom_point() +
        geom_smooth(method='lm')
)

```

