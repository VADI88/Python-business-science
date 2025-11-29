# Plotting Imports
import mizani.formatters as ml
import numpy as np
import pandas as pd
from plotnine import aes
from plotnine.facets.facet_wrap import facet_wrap
from plotnine.geoms import geom_line
from plotnine.geoms.geom_ribbon import geom_ribbon
from plotnine.ggplot import ggplot
from plotnine.labels import labs
from plotnine.scales.scale_manual import scale_color_manual
from plotnine.scales.scale_xy import scale_x_datetime, scale_y_continuous
from plotnine.themes import theme
from plotnine.themes.theme_minimal import theme_minimal
from plydata.cat_tools import cat_reorder  # type: ignore


def plot_forecast(
    data,
    id_column,
    date_column,
    facet_ncol=1,
    facet_scales="free_y",
    date_labels="%Y",
    date_breaks="1 year",
    ribbon_alpha=0.2,
    wspace=0.25,
    figure_size=(16, 8),
    title="Forecast Plot",
    xlab="Date",
    ylab="Revenue",
):
    """Automates the forecast visualization

    Args:
        data (DataFrame): A pandas data frame that is the output
            of the arima_forecast() function.
        id_column (str): [description]
        date_column (str): The timestamp column.
        facet_ncol (int, optional): Number of faceting columns. Defaults to 1.
        facet_scales (str, optional): One of None, "free", "free_y", "free_x". Defaults to "free_y".
        date_labels (str, optional): The strftime format for the x-axis date label. Defaults to "%Y".
        date_breaks (str, optional): Locations for the date breaks on the x-axis. Defaults to "1 year".
        ribbon_alpha (float, optional): The opacity of the confidence intervals. Defaults to 0.2.
        wspace (float, optional): The whitespace to include between subplots. Defaults to 0.25.
        figure_size (tuple, optional): The aspect ratio for the plot. Defaults to (16,8).
        title (str, optional): The plot title. Defaults to "Forecast Plot".
        xlab (str, optional): The x-axis label. Defaults to "Date".
        ylab (str, optional): The y-axis label. Defaults to "Revenue".

    Returns:
        [gglot]: Returns a plotnine ggplot object
    """

    arima_forecast_df = data

    required_columns = [
        id_column,
        date_column,
        "value",
        "prediction",
        "ci_lo",
        "ci_hi",
    ]

    # Data Wrangling
    df_prepped = (
        arima_forecast_df.loc[:, required_columns]
        .melt(
            value_vars=["value", "prediction"],
            id_vars=[id_column, date_column, "ci_lo", "ci_hi"],
            # var_name   = ".variable",
            value_name=".value",
        )
        .rename({".value": "value"}, axis=1)
    )

    # Handle the Categorical Conversion

    df_prepped[id_column] = cat_reorder(
        c=pd.Categorical(df_prepped[id_column]),
        x=df_prepped["value"],
        fun=np.mean,
        ascending=False,
    )

    df_prepped = convert_to_datetime(df_prepped, date_column)

    # Preparing the Plot

    # Geometries
    g = (
        ggplot(
            mapping=aes(x=date_column, y="value", color="variable"),
            data=df_prepped,
        )
        + geom_ribbon(
            aes(ymin="ci_lo", ymax="ci_hi"), alpha=ribbon_alpha, color=None
        )
        + geom_line()
        + facet_wrap(id_column, ncol=facet_ncol, scales=facet_scales)
    )

    # Scales
    g = (
        g
        + scale_x_datetime(date_labels=date_labels, date_breaks=date_breaks)
        + scale_y_continuous(labels=ml.label_dollar(big_mark=",", precision=0))
        + scale_color_manual(values=["red", "#2C3E50"])
    )

    # Theme and Labels
    g = (
        g
        + theme_minimal()
        + theme(
            legend_position="none",
            subplots_adjust={"wspace": wspace},
            figure_size=figure_size,
        )
        + labs(title=title, x=xlab, y=ylab)
    )

    return g


def convert_to_datetime(df_prepped, date_column):
    # Check for period, convert to datetime64
    if df_prepped[date_column].dtype != "datetime64[ns]":
        # Try changing to timestamp
        try:
            df_prepped[date_column] = df_prepped[date_column].dt.to_timestamp()
        except ValueError:
            try:
                df_prepped[date_column] = pd.to_datetime(
                    df_prepped[date_column]
                )
            except ValueError:
                raise Exception(
                    "Could not auto-convert `date_column` to datetime64."
                )
    return df_prepped
