import pandas as pd


# 1. load data
# 2. date format: Date(YYYY), Period（AUS/CHI OBE; AUS/CHI UNDER）, --> YEAR
# FDI world 1960, Gov Consum world 1960, Renew Energy world 1960, Tourism world 1960, UR world 1960;
# GHG world 1990;
# UR CHI 2002-2014；
# 3. Keep Countries
# 4. Year Range Select：i.e., AUS 1995-2005；CHI 2003-2013


# works for 2 GDP csv with date format YYYY/MM/DD (KOR, UK)
def normalize_date(df, date_column):
    """
    Change different date format to YYYY
    :param df:pd.DataFrame
    :param date_column: which column to normalize
    :return: pd.DataFrame
    >>> import pandas as pd
    >>> data = {'Date': ['2020-01-01', '2021-12-31', '01/01/2022', 'InvalidDate']}
    >>> test_df = pd.DataFrame(data)
    >>> result = normalize_date(test_df, 'Date')
    >>> result
          Date
    0    2020
    1    2021
    2    2022
    3     NaN
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.year # if invalid, use NaT
    return df


# works for 6 world csv, to extract only selected countries
def filter_by_country(df, country_column, countries):
    """
    Keep only required countries (Australia, China)
    :param df: pd.DataFrame
    :param country_column: which column to filter
    :param countries: list of countries
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> data = {'Country': ['Australia', 'China', 'Canada', 'Greece'], 'Value': [1, 2, 3, 4]}
    >>> test_df = pd.DataFrame(data)
    >>> result = filter_by_country(test_df, 'Country', ['Australia', 'China'])
    >>> result
        Country  Value
    0  Australia      1
    1      China      2
    """
    return df[df[country_column].isin(countries)]


# for most csv. Must implement after normalize date (so only YYYY left)
# extract year range (10 year window)
def filter_by_year_range(df, year_column, year_range):
    """
    Keep only required year range
    :param df: pd.DataFrame
    :param year_column: which column to filter
    :param year_range: year range
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> data = {'Year': [1990, 1995, 2000, 2005, 2010], 'Value': [10, 15, 20, 25, 30]}
    >>> test_df = pd.DataFrame(data)
    >>> result = filter_by_year_range(test_df, 'Year', (1995, 2005))
    >>> result
        Year  Value
    1  1995     15
    2  2000     20
    3  2005     25
    """
    start_year, end_year = year_range
    return df[(df[year_column] >= start_year) & (df[year_column] <= end_year)]


# for GDP per capita (FDI is still in current US$ total)
def convert_values(df, value_column, convert_to_billion=False, convert_to_million=False, column_label="Value"):
    """
    Convert values to billions or millions and rename column dynamically.

    :param df: pd.DataFrame
    :param value_column: which column to convert
    :param convert_to_billion: whether to convert values to billions
    :param convert_to_million: whether to convert values to millions
    :param column_label: new label for the column (e.g., "GDP", "FDI")
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> data = {'Value': [1e9, 2e9, 3e9]}  # Values in billions
    >>> test_df = pd.DataFrame(data)
    >>> # Convert to billions and rename column to "GDP"
    >>> result = convert_values(test_df, 'Value', convert_to_billion=True, column_label="GDP")
    >>> result
       GDP
    0   1.0
    1   2.0
    2   3.0
    """
    if convert_to_billion and convert_to_million:
        raise ValueError("Only one of 'convert_to_billion' or 'convert_to_million' can be True.")

    if convert_to_billion:
        df[value_column] = df[value_column] / 1e9  # Convert to billions
        df.rename(columns={value_column: column_label}, inplace=True)

    if convert_to_million:
        df[value_column] = df[value_column] / 1e6
        df.rename(columns={value_column: column_label}, inplace=True)
    return df


def preprocess_csv_type1(
    file_path, date_column, year_column, year_range,
    value_column=None, skip_rows=None, convert_to_million=False, convert_to_billion=False, column_label=None):
    """
    To process csv type 1, which is for country with 'Date' column.
    :param file_path: csv file path
    :param date_column: which column to normalize
    :param year_column: which column to filter
    :param year_range: year range
    :param value_column: which column to convert
    :param skip_rows: skip rows until column name occurs
    :param convert_to_million: whether to convert values to millions
    :param convert_to_billion: whether to convert values to billions
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> from io import StringIO
    >>> csv_data = '''
    ... Date,Value
    ... 2001-01-01,1000000000
    ... 2002-01-01,2000000000
    ... 2003-01-01,3000000000
    ... '''
    >>> test_file = StringIO(csv_data)  # Simulate a CSV file with StringIO
    >>> result = preprocess_csv_type1(
    ...     file_path=test_file,
    ...     date_column="Date",
    ...     year_column="Year",
    ...     year_range=(2002, 2003),
    ...     value_column="Value",
    ...     convert_to_billion=True,
    ...     column_label="GDP"
    ... )
    >>> result
       Year  GDP
    1  2002  2.0
    2  2003  3.0
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = normalize_date(df, date_column)
    df = filter_by_year_range(df, year_column, year_range)

    if value_column and (convert_to_billion or convert_to_million):
        if column_label is None:
            raise ValueError("`column_label` must be provided when converting values.")
        df = convert_values(
            df, value_column,
            convert_to_billion=convert_to_billion,
            convert_to_million=convert_to_million,
            column_label=column_label
        )
    df.columns = df.columns.str.strip()
    return df


def preprocess_csv_type2(file_path, country_column, countries, year_column, year_range, skip_rows=None):
    """
    To process csv type 2, which is for country with 'Period' column.
    :param file_path: csv file path
    :param country_column: which column to convert
    :param countries: list of countries
    :param year_column: which column to normalize
    :param year_range: year range
    :param skip_rows: skip rows until column name occurs
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> from io import StringIO
    >>> csv_data = '''
    ... Location,Period,Dim1,Value
    ... Australia,2000,Female,30.5 [info]
    ... Australia,2001,Male,29.7 [note]
    ... China,2000,Female,25.1 [data]
    ... China,2001,Male,24.9 [info]
    ... '''
    >>> test_file = StringIO(csv_data)  # Simulate a CSV file with StringIO
    >>> result = preprocess_csv_type2(
    ...     file_path=test_file,
    ...     country_column="Location",
    ...     countries=["Australia"],
    ...     year_column="Period",
    ...     year_range=(2000, 2001),
    ...     skip_rows=None
    ... )
    >>> result
        Location  Period    Dim1  Value
    0  Australia    2000  Female   30.5
    1  Australia    2001    Male   29.7
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = filter_by_country(df, country_column, countries)
    df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
    df = filter_by_year_range(df, year_column, year_range)

    # Keep only Value, Location, Period cols
    df = df[[country_column, year_column,'Dim1', 'Value']]

    # Clean the 'Value' column to remove text inside brackets
    df['Value'] = df['Value'].apply(lambda x: str(x).split('[')[0].strip())
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.columns = df.columns.str.strip()
    return df


def preprocess_csv_type3(
        file_path, country_column, countries, year_column, year_range,
        skip_rows=None, value_column=None, convert_to_million=False, convert_to_billion=False, column_label=None):
    """
    To process csv type 3, which doesn't have a column named Date, but every year as 1 column (the WorldBank csvs).
    :param file_path: csv file path
    :param country_column: which column to select
    :param countries: list of countries
    :param year_column: which column to select
    :param year_range: year range
    :param skip_rows: skip rows until column name occurs
    :param value_column: which column to convert
    :param convert_to_million: whether to convert values to millions
    :param convert_to_billion: whether to convert values to billions
    :param column_label: new label for the column
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> from io import StringIO
    >>> csv_data = '''
    ... Country Name,2000,2001,2002
    ... Australia,1000000000,1100000000,1200000000
    ... China,2000000000,2100000000,2200000000
    ... '''
    >>> test_file = StringIO(csv_data)  # Simulate a CSV file with StringIO
    >>> result = preprocess_csv_type3(
    ...     file_path=test_file,
    ...     country_column="Country Name",
    ...     countries=["Australia"],
    ...     year_column="Year",
    ...     year_range=(2000, 2002),
    ...     value_column="Value",
    ...     convert_to_billion=True,
    ...     column_label="GDP"
    ... )
    >>> result
      Country Name  Year  GDP
    0    Australia  2000  1.0
    1    Australia  2001  1.1
    2    Australia  2002  1.2
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = filter_by_country(df, country_column, countries)

    year_columns = [col for col in df.columns if col.isdigit()]  # col name?

    df = pd.melt(df, id_vars=[country_column], value_vars=year_columns,
                 var_name=year_column, value_name='Value')  # wide -> long table

    df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
    df = filter_by_year_range(df, year_column, year_range)

    if value_column and (convert_to_billion or convert_to_million):
        if column_label is None:
            raise ValueError("`column_label` must be provided when converting values.")
        df = convert_values(
            df, value_column,
            convert_to_billion=convert_to_billion,
            convert_to_million=convert_to_million,
            column_label=column_label
        )
    df.columns = df.columns.str.strip()
    return df


def preprocess_special_csv(file_path, year_column, year_range, skip_rows=None):
    """
    Special process for csv which doesn't have a column named Date, and contain only 1 country.
    :param file_path: csv file path
    :param year_column: which column to select
    :param year_range: year range
    :param skip_rows: skip rows until column name occurs
    :return: pd.DataFrame

    >>> import pandas as pd
    >>> from io import StringIO
    >>> csv_data = '''
    ... Indicator,2002,2003,2004,2005,2006
    ... Unemployment Rate,5.0,5.2,5.1,5.3,5.4
    ... GDP Growth,3.0,3.1,3.2,3.4,3.5
    ... '''
    >>> test_file = StringIO(csv_data)  # Simulate a file with StringIO
    >>> result = preprocess_special_csv(
    ...     file_path=test_file,
    ...     year_column="Year",
    ...     year_range=(2003, 2005),
    ...     skip_rows=0
    ... )
    >>> result
           Indicator  Year  Value
    1  Unemployment Rate  2003   5.2
    2  Unemployment Rate  2004   5.1
    3  Unemployment Rate  2005   5.3
    """
    df = pd.read_csv(file_path, skiprows=skip_rows, encoding='latin1')

    df.columns = ['Indicator'] + [str(year) for year in range(2002, 2016)]
    df = pd.melt(df, id_vars=['Indicator'], var_name=year_column, value_name='Value')
    df = df[df['Indicator'].str.contains('Unemployment Rate', case=False, na=False)]
    df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
    df = filter_by_year_range(df, year_column, year_range)
    return df


if __name__ == '__main__':
    AUS_GDP = preprocess_csv_type1(
        file_path='data/australia-gdp-gross-domestic-product.csv',
        date_column='Date',
        year_column='Date',
        year_range=(1995, 2005),
        skip_rows=7  # Skip the first 6 rows to start from the correct header
    )
    #print(AUS_GDP)   # test success

    CHI_GDP = preprocess_csv_type1(
        file_path='data/China-gdp.csv',
        date_column='DATE',
        year_column='DATE',
        year_range=(2003, 2013),
        value_column='MKTGDPCNA646NWDB',
        skip_rows=0,
        convert_to_billion=True,
        column_label='GDP'
    )
    #print(CHI_GDP)  # test success

    AUS_FDI = preprocess_csv_type3(
        file_path='data/Foreign_Direct _Investment.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995,2005),
        skip_rows=3,
        value_column='Value',
        convert_to_billion=True,
        column_label='FDI'
    )
    #print(AUS_FDI)  # test success

    CHI_FDI = preprocess_csv_type3(
        file_path='data/Foreign_Direct _Investment.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003,2013),
        skip_rows=3,
        value_column='Value',
        convert_to_billion=True,
        column_label='FDI'
    )
    #print(CHI_FDI)  # test success

    AUS_gov_consume = preprocess_csv_type3(
        file_path='data/Government_consumption.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=3,
        value_column='Value',
        convert_to_billion=True,
        column_label='Gov_Consumption'
    )
    #print(AUS_gov_consume)  # test success

    CHI_gov_consume = preprocess_csv_type3(
        file_path='data/Government_consumption.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=3,
        value_column='Value',
        convert_to_billion=True,
        column_label='Gov_Consumption'
    )
    #print(CHI_gov_consume)  # test success

    AUS_tourism = preprocess_csv_type3(
        file_path='data/tourism_data.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=3,
        value_column='Value',
        convert_to_million=True,
        column_label='Tourism'
    )
    #print(AUS_tourism)  # test success

    CHI_tourism = preprocess_csv_type3(
        file_path='data/tourism_data.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=3,
        value_column='Value',
        convert_to_million=True,
        column_label='Tourism'
    )
    #print(CHI_tourism)  # test success

    AUS_obesity = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['Australia'],
        year_column='Period',
        year_range=(1995, 2005),
        skip_rows=0
    )
    #print(AUS_obesity)  # test success

    CHI_obesity = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['China'],
        year_column='Period',
        year_range=(2003,2013),
        skip_rows=0
    )
    #print(CHI_obesity)  # test success

    AUS_underweight = preprocess_csv_type2(
        file_path='data/Prevalence_of_underweight_among_adults.csv',
        country_column='Location',
        countries=['Australia'],
        year_column='Period',
        year_range=(1995, 2005),
        skip_rows=0
    )
    print(AUS_underweight)  # test success

    CHI_underweight = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['China'],
        year_column='Period',
        year_range=(2003, 2013),
        skip_rows=0
    )
    print(CHI_underweight)  # test success


    AUS_GHG_emission = preprocess_csv_type3(
        file_path='data/ghg-emissions.csv',
        country_column='Country/Region',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995,2005)
    )
    #print(AUS_GHG_emission)  # test success

    CHI_GHG_emission = preprocess_csv_type3(
        file_path='data/ghg-emissions.csv',
        country_column='Country/Region',
        countries=['China'],
        year_column='Year',
        year_range=(2003,2013)
    )
    #print(CHI_GHG_emission)  # test success

    AUS_renew_energy = preprocess_csv_type3(
        file_path='data/Renewable_energy_consumption.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=3
    )
    #print(AUS_renew_energy)  # test success

    CHI_renew_energy = preprocess_csv_type3(
        file_path='data/Renewable_energy_consumption.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=3
    )
    #print(CHI_renew_energy)  # test success


    AUS_UR = preprocess_csv_type3(
        file_path='data/Unemployment_rate_Australia.csv.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=4
    )
    #print(AUS_UR)  # test success

    CHI_UR = preprocess_special_csv(
        file_path='data/Unemployment_rate_China.csv',
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=2
    )
    #print(CHI_UR)  # test success





