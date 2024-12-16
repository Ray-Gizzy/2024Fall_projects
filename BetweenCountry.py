import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import numpy as np

def calculate_growth_rate(df, metric_column):
    """
    Calculate the growth rate for GDP or FDI per year.

    :param df: a cleaned dataframe
    :param metric_column: the GDP/FDI column
    :return: DataFrame with an additional column 'Growth Rate (%)'
        Example:
    >>> import pandas as pd
    >>> data = {'Year': [2000, 2001, 2002], 'GDP': [1000, 1100, 1210]}
    >>> df = pd.DataFrame(data)
    >>> calculate_growth_rate(df, 'GDP')
       Year   GDP  Growth Rate (%)
    0  2000  1000         0.000000
    1  2001  1100        10.000000
    2  2002  1210        10.000000
    """
    growth_rates = [0]

    for i in range(1, len(df)):
        previous_year = df.loc[i - 1, metric_column]  # row:i-1, col: metric
        current_year = df.loc[i, metric_column]

        if previous_year == 0 or not isinstance(current_year, (int, float)) or not isinstance(previous_year, (int, float)):
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
    :param host_year: the hosting year for alignment (e.g., 2000 or 2008)
    :param metric_column: GDP or FDI column to apply the "calculate_growth_rate" function
    :return: cleaned DataFrame

    >>> import pandas as pd
    >>> data = {'Year': [1999, 2000, 2001], 'GDP': [1000, 1100, 1210]}
    >>> test_df = pd.DataFrame(data)
    >>> result = index_rename_and_calculate_growth_rate(
    ...     test_df, rename_dict={'GDP': 'GDP_per_capita'}, host_year=2000, metric_column='GDP_per_capita'
    ... )
    >>> result[['Year', 'GDP_per_capita', 'Growth Rate (%)', 'Relative Year']]
       Year  GDP_per_capita  Growth Rate (%)  Relative Year
    0  1999          1000.0         0.000000             -1
    1  2000          1100.0        10.000000              0
    2  2001          1210.0        10.000000              1
    """
    # Handle empty DataFrame
    if df.empty:
        print(f"Warning: Input DataFrame is empty for host year {host_year}.")
        return pd.DataFrame({
            'Country': [rename_dict.get('Country', 'Unknown')],
            'Year': [host_year],
            metric_column: [0],
            'Relative Year': [0],
            'Growth Rate (%)': [0]
        })

    df.reset_index(inplace=True, drop=True)  # Ensure continuous index
    df.columns = df.columns.str.strip()

    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)

    if 'Year' not in df.columns:
        raise ValueError("The DataFrame does not have a 'Year' column. Please check the data.")

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Convert to numeric, invalid rows become NaN
    df.dropna(subset=['Year'], inplace=True)  # Drop rows with invalid Year
    df['Year'] = df['Year'].astype(int)  # Ensure Year is integer

    if len(df) < 2:
        raise ValueError("The DataFrame has insufficient rows for processing.")

    if df['Year'].iloc[0] > df['Year'].iloc[-1]:  # High to Low
        df.sort_values(by='Year', inplace=True)  # Sort ascending

    # Check if host_year is within the Year range
    if host_year not in df['Year'].values:
        print(f"Warning: Host year {host_year} not found in the Year column for this dataset.")
        return pd.DataFrame({
            'Country': [rename_dict.get('Country', 'Unknown')],
            'Year': [host_year],
            metric_column: [0],
            'Relative Year': [0],
            'Growth Rate (%)': [0]
        })

    calculate_growth_rate(df, metric_column=metric_column)  # Ensure this function works correctly
    df['Relative Year'] = df['Year'] - host_year

    return df


def growth_rate_plot(dfs, countries, metric, colors=None):
    """
    Plot the growth rate for up to eight countries.

    :param dfs: List of dataframes from "index_rename_and_calculate_growth_rate".
    :param countries: List of countries to compare growth rates.
    :param metric: Column to compare growth rates.
    :param colors: List of colors for each country's line (optional).
    >>> import pandas as pd
    >>> test_data1 = {'Relative Year': [-1, 0, 1], 'Growth Rate (%)': [5.0, 10.0, 8.0]}
    >>> test_data2 = {'Relative Year': [-1, 0, 1], 'Growth Rate (%)': [3.0, 6.0, 7.0]}
    >>> df1 = pd.DataFrame(test_data1)
    >>> df2 = pd.DataFrame(test_data2)
    >>> growth_rate_plot(
    ...     dfs=[df1, df2],
    ...     countries=["Country A", "Country B"],
    ...     metric="GDP",
    ...     colors=['blue', 'orange']
    ... )
    """
    if colors is None:
        # Generate a default color palette
        colors = ['blue', 'yellow', 'green', 'purple', 'orange', 'pink', 'cyan', 'brown']

    plt.figure(figsize=(12, 8))  # Adjust size for better visualization

    for df, country, color in zip(dfs, countries, colors[:len(countries)]):
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


import matplotlib.pyplot as plt


def eight_subplots(dataframes, host_years, legends, titles, x_column, y_column, xlabel, ylabel):
    """
    Plot 8 subplots for given dataframes and metrics.

    :param dataframes: List of 8 DataFrames for the plots.
    :param host_years: List of 8 years for the vertical reference lines.
    :param legends: List of 8 legends for each plot.
    :param titles: List of 8 titles for each subplot.
    :param x_column: Column name for the x-axis.
    :param y_column: Column name for the y-axis.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    >>> import pandas as pd
    >>> test_data = {'Year': [1995, 1996, 1997, 1998, 1999], 'Value': [10, 12, 15, 14, 18]}
    >>> df1 = pd.DataFrame(test_data)
    >>> df2 = pd.DataFrame(test_data)
    >>> dataframes = [df1, df2] + [None] * 6  # 2 valid DataFrames, 6 placeholders
    >>> host_years = [1997, 1997] + [None] * 6
    >>> legends = ["Test Plot 1", "Test Plot 2"] + ["No Data"] * 6
    >>> titles = ["Title 1", "Title 2"] + ["No Data"] * 6
    >>> eight_subplots(
    ...     dataframes=dataframes,
    ...     host_years=host_years,
    ...     legends=legends,
    ...     titles=titles,
    ...     x_column="Year",
    ...     y_column="Value",
    ...     xlabel="Year",
    ...     ylabel="Test Value"
    ... )
    """


    plt.figure(figsize=(16, 12))  # Adjust figure size

    for i in range(8):
        plt.subplot(4, 2, i + 1)  # 4 rows, 2 columns, subplot index
        df = dataframes[i]
        host_year = host_years[i]
        legend = legends[i]
        title = titles[i]

        if df.empty:
            plt.text(0.5, 0.5, "No Data Available", fontsize=12, ha='center', va='center')
            plt.title(title)
            plt.axis('off')
            continue

        # Ensure y_column is numeric
        if not np.issubdtype(df[y_column].dtype, np.number):
            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')

        plt.plot(df[x_column], df[y_column], label=legend, marker='o', color=f'C{i % 10}')  # Different colors
        plt.axvline(x=host_year, color='red', linestyle='--', label=f'{host_year} Event')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()

    # Adjust layout and show
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    plt.show()


def four_plot_health(
        dfs, host_years, titles, x_column, y_column, xlabel, ylabel, metric, gender_column):
    """
    Compare health trends for four countries using three gender categories.

    :param dfs: List of DataFrames for the countries.
    :param host_years: List of host years for the countries.
    :param titles: List of titles for the plots.
    :param x_column: Column name for the x-axis.
    :param y_column: Column name for the y-axis.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param metric: Column to compare health trends.
    :param gender_column: Column name for the gender categories.
    """
    genders = ['Female', 'Male', 'Both sexes']
    colors = ['blue', 'orange', 'green']

    plt.figure(figsize=(14, 10))  # Adjust size for 4 subplots

    for i, (df, host_year, title) in enumerate(zip(dfs, host_years, titles), 1):
        plt.subplot(2, 2, i)  # 2 rows, 2 columns, subplot i
        for gender, color in zip(genders, colors):
            gender_data = df[df[gender_column] == gender]
            plt.plot(
                gender_data[x_column],
                gender_data[y_column],
                label=f'{gender} {metric}',
                marker='o',
                color=color
            )
        plt.axvline(x=host_year, color='red', linestyle='--', label=f'{host_year} Olympics')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()

    plt.tight_layout()
    plt.show()


def load_and_merge_data(cleaned_data_dict):
    """
    Load and merge cleaned data dynamically based on the provided dictionary.

    :param cleaned_data_dict: Dictionary with metric names as keys and a nested dictionary
                              containing "AUS" and "CHI" DataFrames.
    :return: Merged DataFrame with country-specific columns.
    """
    merged_data = pd.DataFrame()

    for metric_name, country_data in cleaned_data_dict.items():
        aus_data = country_data["AUS"]
        chi_data = country_data["CHI"]

        # Select relevant columns and rename for each country
        aus_data = aus_data[["Relative Year", metric_name]].rename(columns={metric_name: f"{metric_name}_AUS"})
        chi_data = chi_data[["Relative Year", metric_name]].rename(columns={metric_name: f"{metric_name}_CHI"})

        if merged_data.empty:
            # Initialize merged_data with the first metric
            merged_data = aus_data.merge(chi_data, on="Relative Year", how="left")
        else:
            # Merge subsequent metrics
            merged_data = merged_data.merge(aus_data, on="Relative Year", how="left")
            merged_data = merged_data.merge(chi_data, on="Relative Year", how="left")

    return merged_data


def calculate_correlation(df, metrics, time_period=None):
    """
    Calculate correlation between metrics within a specific time period.

    :param df: DataFrame containing metrics
    :param metrics: List of column names for metrics to analyze
    :param time_period: Tuple (start, end) to filter by Relative Year
    :return: Correlation matrix
    """
    if time_period:
        df = df[df['Relative Year'].between(*time_period)]
    return df[metrics].corr()


metric_groups = {
    "Economic": ["GDP_per_capita", "FDI", "Gov_Consumption"],
    "Social": ["Num_Arrivals", "Obesity_rate", "Underweight_rate", "Unemployment_Rate(%)"],
    "Environmental": ["MtCO2e"]
}

country_suffix = {"Australia": "_AUS", "China": "_CHI"}


def compute_country_correlation_matrices(merged_data, metric_groups, country_suffix):
    """
    Compute correlation matrices for each country and each metric group.

    :param merged_data: DataFrame with merged country metrics.
    :param metric_groups: Dictionary of metric groups and their metrics.
    :param country_suffix: Dictionary mapping country names to their column suffixes.
    :return: Dictionary containing correlation matrices for each country and group.
    """
    correlation_matrices = {country: {} for country in country_suffix}

    for country, suffix in country_suffix.items():
        print(f"\nComputing correlation matrices for {country}:")
        for group, metrics in metric_groups.items():
            group_columns = [f"{metric}{suffix}" for metric in metrics if f"{metric}{suffix}" in merged_data.columns]
            if len(group_columns) > 1:
                group_corr = calculate_correlation(merged_data, group_columns, time_period=(-5, 5))
                correlation_matrices[country][group] = group_corr
                print(f"\n{group} Correlation Matrix for {country}:")
                print(group_corr)
            else:
                print(f"Not enough data for {group} metrics in {country}.")
    return correlation_matrices


def plot_correlation_heatmap(correlation_matrix, title="Correlation Heatmap"):
    """
    Plot a heatmap for the given correlation matrix.

    :param correlation_matrix: Correlation matrix (Pandas DataFrame)
    :param title: Title for the heatmap
    """

    if correlation_matrix is not None and not correlation_matrix.empty:
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title(title, fontsize=16)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No data available to plot heatmap: {title}")


def plot_all_heatmaps(correlation_matrices, metric_groups):
    """
    Plot heatmaps for each country and metric group.

    :param correlation_matrices: Dictionary containing correlation matrices by country.
    :param metric_groups: Dictionary defining the metric groups (e.g., Economic, Social).
    """
    for country, group_data in correlation_matrices.items():
        print(f"Generating heatmaps for {country}:")
        for group, group_corr in group_data.items():
            if group_corr is not None:  # Ensure there is a valid correlation matrix
                title = f"{group} Metric Correlation ({country})"
                plot_correlation_heatmap(group_corr, title=title)
            else:
                print(f"Not enough data for {group} metrics in {country}.")


# Define predefined combinations with descriptions
predefined_combinations = {
    "1": {
        "description": "Do GDP and FDI correlated?",
        "metrics": ("GDP_per_capita", "FDI")
    },
    "2": {
        "description": "How does fiscal policy impact government consumption?",
        "metrics": ("GDP_per_capita", "Gov_Consumption")
    },
    "3": {
        "description": "Does tourism impact economic growth?",
        "metrics": ("Num_Arrivals", "GDP_per_capita")
    },
    "4": {
        "description": "Health trade-offs",
        "metrics": ("Obesity_rate", "Underweight_rate")
    },
    "5": {
        "description": "Environmental cost of economic growth",
        "metrics": ("GDP_per_capita", "MtCO2e")
    },
    "6": {
        "description": "Does increasing tourism lead to higher GHG emission?",
        "metrics": ("Num_Arrivals", "MtCO2e")
    },
    "7": {
        "description": "Economic growth's effect on employment",
        "metrics": ("Unemployment_Rate(%)", "GDP_per_capita")
    }
}


def predefined_correlation_analysis(merged_data):
    # Display the menu with descriptions first
    print("\nAvailable Metric Combinations:")
    for key, combination in predefined_combinations.items():
        print(f"{key}: {combination['description']}")

    # Add a short delay to ensure the output is printed before input prompt
    time.sleep(0.5)

    # User selects a combination
    selected_key = input("\nChoose a combination number (e.g., 1): ").strip()
    if selected_key not in predefined_combinations:
        print("Invalid selection!")
        return

    combination = predefined_combinations[selected_key]
    metric1, metric2 = combination["metrics"]
    print(f"\nSelected combination: {combination['description']}")

    # User selects a country suffix
    country = input("Select a country suffix (AUS or CHI): ").strip().upper()
    if country not in ["AUS", "CHI"]:
        print("Invalid country suffix!")
        return

    suffix = f"_{country}"
    print(f"\nSelected country suffix: {country}")

    # Check if the selected metrics exist directly in merged_data
    metric1_col = f"{metric1}{suffix}"
    metric2_col = f"{metric2}{suffix}"
    print(f"Checking columns: {metric1_col} and {metric2_col}")

    if metric1_col not in merged_data.columns or metric2_col not in merged_data.columns:
        print(f"Missing: {metric1_col} or {metric2_col} in {country}. Cannot calculate correlation.")
        return

    # Calculate correlation
    correlation_value = merged_data[[metric1_col, metric2_col]].corr().iloc[0, 1]
    print(f"\nCorrelation between {metric1} and {metric2} in {country}: {correlation_value:.2f}")

    # Visualization (optional)
    plt.figure(figsize=(6, 4))
    plt.scatter(merged_data[metric1_col], merged_data[metric2_col], alpha=0.6, edgecolor='k')
    plt.title(f"Correlation between {metric1} and {metric2} in {country}")
    plt.xlabel(metric1)
    plt.ylabel(metric2)
    plt.grid(True)
    plt.show()


def highlight_key_correlations_all_matrices(correlation_matrices, country):
    """
    Highlight the strongest and weakest correlations across all metric group matrices for a given country.

    :param correlation_matrices: Dictionary of correlation matrices (key: group name, value: DataFrame)
    :param country: Country name (e.g., "Australia", "China")
    """
    print(f"\n=== Highlighting Key Correlations for {country} ===")

    for group, matrix in correlation_matrices.items():
        # Flatten the matrix for easier analysis (ignore diagonal)
        flattened = matrix.where(~np.eye(matrix.shape[0], dtype=bool))

        strongest_pair = flattened.unstack().idxmax()
        weakest_pair = flattened.unstack().idxmin()

        strongest_value = flattened.unstack().max()
        weakest_value = flattened.unstack().min()

        print(f"\n{group} Correlation Matrix:")
        print(f"  Strongest correlation: {strongest_pair} = {strongest_value:.2f}")
        print(f"  Weakest correlation: {weakest_pair} = {weakest_value:.2f}")


def plot_predefined_combinations_bar(predefined_combinations, merged_data):
    """
    Computes correlations for predefined combinations and plots a bar chart.

    :param predefined_combinations: Dictionary of metric pairs and descriptions.
    :param merged_data: DataFrame containing merged data with metrics for both countries.
    """
    correlations = []

    for key, combo in predefined_combinations.items():
        metric1, metric2 = combo["metrics"]

        # Check if the metrics exist in the merged_data
        for country_suffix in ["_AUS", "_CHI"]:
            metric1_col = f"{metric1}{country_suffix}"
            metric2_col = f"{metric2}{country_suffix}"

            if metric1_col in merged_data.columns and metric2_col in merged_data.columns:
                # Compute correlation
                corr_value = merged_data[[metric1_col, metric2_col]].corr().iloc[0, 1]
                correlations.append({
                    "Combination": f"{metric1} vs {metric2}",
                    "Country": "Australia" if country_suffix == "_AUS" else "China",
                    "Correlation": corr_value
                })
            else:
                print(f"Missing: {metric1_col} or {metric2_col} in {country_suffix.replace('_', '')}")

    # Create DataFrame for plotting
    corr_df = pd.DataFrame(correlations)

    # Create bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=corr_df, x="Combination", y="Correlation", hue="Country", dodge=True)
    plt.title("Correlation Strengths for Predefined Metric Pairs")
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.ylabel("Correlation Coefficient")
    plt.xlabel("Metric Pairs")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Country")
    plt.tight_layout()
    plt.show()



