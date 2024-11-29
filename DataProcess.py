import pandas as pd


# 1. load data
# 2. date format: Date(AUS GDP:年末；CHI GDP:年初), Period（AUS/CHI OBE; AUS/CHI UNDER）, --> YEAR
# FDI world 1960, Gov Consum world 1960, Renew Energy world 1960, Tourism world 1960, UR world 1960;
# GHG world 1990;
# UR CHI 2002-2014；
# 3. 保留国家
# 4. 年份： AUS 1995-2005；CHI 2003-2013


# works for 2 GDP csv
def normalize_date(df, date_column):
    """
    Change different date format to YYYY
    :param df:pd.DataFrame
    :param date_column: which column to normalize
    :return: pd.DataFrame
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.year # if invalid, use NaT
    return df


# works for 6 world csv
def filter_by_country(df, country_column, countries):
    """
    Keep only required countries (Australia, China)
    :param df: pd.DataFrame
    :param country_column: which column to filter
    :param countries: list of countries
    :return: pd.DataFrame
    """
    return df[df[country_column].isin(countries)]


# for 6 world csv, convert year in column to year in row
def reshape_dataset(df, id_vars, value_vars):
    """
    For dataset where year is in the first row, convert it to year in column
    :param df: pd.DataFrame
    :param id_vars: column kept
    :param value_vars: column need to change
    :return: pd.DataFrame
    """
    return pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                   var_name='Year', value_name='Value').astype({'Year': int})


# for all csv. Must implement after normalize date (so only YYYY left)
def filter_by_year_range(df, year_column, year_range):
    """
    Keep only required year range (Australia 1995-2005, China 2003-2013 --> 1995-2013)
    :param df: pd.DataFrame
    :param year_column: which column to filter
    :param year_range: year range
    :return: pd.DataFrame
    """
    start_year, end_year = year_range
    return df[(df[year_column] >= start_year) & (df[year_column] <= end_year)]


def convert_gdp(df, value_column, convert_to_billion=False):
    """
    Convert values to billions.
    :param df: pd.DataFrame
    :param value_column: which column to convert
    :param convert_to_billion: whether to convert values to billions
    :return: pd.DataFrame
    """

    # Convert GDP values to billions if specified
    if convert_to_billion:
        df[value_column] = df[value_column] / 1e9  # Convert to billions

    # Rename the GDP column to indicate units
    if convert_to_billion:
        df.rename(columns={value_column: f"GDP (Billion)"}, inplace=True)

    return df


def preprocess_csv_type1(file_path, date_column, year_column, year_range, value_column=None, skip_rows=None, convert_to_billion=False):
    """
    To process csv type 1, which is for 1 country with 'Date' column.
    :param file_path: csv file path
    :param date_column: which column to normalize
    :param year_column: which column to filter
    :param year_range: year range
    :param value_column: which column to convert (GDP)
    :param skip_rows: skip rows until column name occurs
    :return: pd.DataFrame
    """

    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = normalize_date(df, date_column)
    df = filter_by_year_range(df, year_column, year_range)
    if value_column and convert_to_billion:
        df = convert_gdp(df, value_column, convert_to_billion=True)
    return df


def preprocess_csv_type2(file_path, country_column, countries, year_column, year_range, skip_rows=None):
    """
    To process csv type 2, which is for 2 country with 'Period' column.
    :param file_path: csv file path
    :param country_column: which column to convert
    :param countries: list of countries
    :param year_column: which column to normalize
    :param year_range: year range
    :param skip_rows: skip rows until column name occurs
    :return: pd.DataFrame
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = filter_by_country(df, country_column, countries)
    df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
    df = filter_by_year_range(df, year_column, year_range)
    return df


def preprocess_csv_type3(file_path, country_column, countries, year_range):
    """
    To process csv type 3, which doesn't have a column named Date, but every year as 1 column.
    :param file_path: csv file path
    :param country_column: which column to select
    :param countries: list of countries
    :param year_range: year range
    :return: pd.DataFrame
    """
    df = pd.read_csv(file_path)
    # 筛选国家
    df = filter_by_country(df, country_column, countries)
    # 转换宽表为长表
    year_columns = [col for col in df.columns if col.isdigit()]  # 自动识别年份列
    df = reshape_dataset(df, id_vars=[country_column], value_vars=year_columns)
    # 筛选年份
    df = filter_by_year_range(df, year_range)
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
        year_range=(2002, 2013),
        value_column='MKTGDPCNA646NWDB',
        skip_rows=0,
        convert_to_billion=True
    )
    #print(CHI_GDP)  # test success

    AUS_OBES = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['Australia'],
        year_column='Period',
        year_range=(1995, 2005),
        skip_rows=0,
    )
    #print(AUS_OBES)  # test success

    CHI_OBES = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['China'],
        year_column='Period',
        year_range=(2003,2013),
        skip_rows=0,
    )
    #print(AUS_OBES)  # test success


