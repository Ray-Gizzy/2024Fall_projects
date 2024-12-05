import matplotlib.pyplot as plt


def calculate_growth_rate(df, metric_column):
    """
    Calculate the growth rate for GDP or FDI per year.

    :param df: a cleaned dataframe
    :param metric_column: the GDP/FDI column
    :return: DataFrame with an additional column 'Growth Rate (%)'
    """
    growth_rates = [0]

    for i in range(1, len(df)):
        previous_year = df.loc[i - 1, metric_column]  # row:i-1, col: metric
        current_year = df.loc[i, metric_column]

        if previous_year == 0:
            growth_rates.append(0)
        else:
            growth_rate = ((current_year - previous_year) / previous_year) * 100
            growth_rates.append(growth_rate)

    df['Growth Rate (%)'] = growth_rates
    return df


def index_rename_and_calculate_growth_rate(df, rename_dict=None, host_year=None, metric_column=None):
    """
    Second clean the data to prepare for growth rate comparison plot.

    :param df: a cleaned dataframe from DataProcess.py
    :param rename_dict: the columns needed to be renamed
    :param host_year: either 2000 or 2008
    :param metric_column: GDP or FDI column to apply the "calculate_growth_rate" function
    :return: cleaned dataFrame
    """
    df.reset_index(inplace=True)
    df.columns = df.columns.str.strip()
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)
    calculate_growth_rate(df, metric_column=metric_column)
    df['Relative Year'] = df['Year'] - host_year
    return df


def growth_rate_plot(dfs, countries, metric, colors):
    """
    Plot the growth rate for countries.

    :param dfs: dataframes from "index_rename_and_calculate_growth_rate"
    :param countries: countries to compare growth rates
    :param metric: GDP/FDI column to compare growth rates
    :param colors: color of line
    """
    if colors is None:
        colors = ['blue', 'yellow']

    plt.figure(figsize=(8, 5))
    for df, country, color in zip(dfs, countries, colors):
        plt.plot(
            df['Relative Year'],
            df['Growth Rate (%)'],
            label=f"{country} {metric} Growth Rate",
            marker='o',
            color=color
        )
    plt.axvline(x=0, color='red', linestyle='--', label='Host Year')
    plt.title(f"{metric} Growth (Relative to Hosting Year)")
    plt.xlabel("Years (Relative to Hosting Year)")
    plt.ylabel(f"{metric} Growth Rate (%)")
    plt.legend()
    plt.grid()
    plt.show()


def two_subplots(
        df1, host_year1, legend1, title1,
        df2, host_year2, legend2, title2,
        x_column, y_column, xlabel, ylabel,
        ):
    """
    Plot two subplots for given dataframes and metrics.

    :param df1: DataFrame for the first plot.
    :param df2: DataFrame for the second plot.
    :param x_column: Column name for the x-axis.
    :param y_column: Column name for the y-axis.
    :param title1: Title for the first subplot.
    :param title2: Title for the second subplot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param legend1: Legend for the first plot.
    :param legend2: Legend for the second plot.
    :param host_year1: 2000
    :param host_year2: 2008
    """

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)  # Subplot 1: 1ROW, 2COLS
    plt.plot(df1[x_column], df1[y_column], label=legend1, marker='o', color='blue')
    plt.axvline(x=host_year1, color='red', linestyle='--', label=f'{host_year1} Olympics')
    plt.title(title1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)  # Subplot 2
    plt.plot(df2[x_column], df2[y_column], label=legend2, marker='o', color='yellow')
    plt.axvline(x=host_year2, color='red', linestyle='--', label=f'{host_year2} Olympics')
    plt.title(title2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    # Adjust layout and show
    plt.tight_layout()
    plt.show()