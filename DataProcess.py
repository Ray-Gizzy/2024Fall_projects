import pandas as pd


# 1. load data
# 2. date format: Date(AUS GDP:年末；CHI GDP:年初), Period（AUS/CHI OBE; AUS/CHI UNDER）, --> YEAR
# FDI world 1960, Gov Consum world 1960, Renew Energy world 1960, Tourism world 1960, UR world 1960;
# GHG world 1990;
# UR CHI 2002-2014；
# 3. 保留国家
# 4. 年份： AUS 1995-2005；CHI 2003-2013


# works for 2 GDP csv with date format YYYY/MM/DD
def normalize_date(df, date_column):
    """
    Change different date format to YYYY
    :param df:pd.DataFrame
    :param date_column: which column to normalize
    :return: pd.DataFrame
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.year # if invalid, use NaT
    return df


# works for 6 world csv, to extract only AUS & CHI
def filter_by_country(df, country_column, countries):
    """
    Keep only required countries (Australia, China)
    :param df: pd.DataFrame
    :param country_column: which column to filter
    :param countries: list of countries
    :return: pd.DataFrame
    """
    return df[df[country_column].isin(countries)]


# for most csv. Must implement after normalize date (so only YYYY left)
# extract Australia 1995-2005, China 2003-2013
def filter_by_year_range(df, year_column, year_range):
    """
    Keep only required year range
    :param df: pd.DataFrame
    :param year_column: which column to filter
    :param year_range: year range
    :return: pd.DataFrame
    """
    start_year, end_year = year_range
    return df[(df[year_column] >= start_year) & (df[year_column] <= end_year)]


def convert_values(df, value_column, convert_to_billion=False, column_label="Value"):
    """
    Convert values to billions and rename column dynamically.

    :param df: pd.DataFrame
    :param value_column: which column to convert
    :param convert_to_billion: whether to convert values to billions
    :param column_label: new label for the column (e.g., "GDP", "FDI")
    :return: pd.DataFrame
    """
    # Convert values to billions if specified
    if convert_to_billion:
        df[value_column] = df[value_column] / 1e9  # Convert to billions

    # Rename the column
    if convert_to_billion:
        df.rename(columns={value_column: column_label}, inplace=True)

    return df


def preprocess_csv_type1(
    file_path, date_column, year_column, year_range,
    value_column=None, skip_rows=None, convert_to_billion=False, column_label=None):
    """
    To process csv type 1, which is for 1 country with 'Date' column.
    :param file_path: csv file path
    :param date_column: which column to normalize
    :param year_column: which column to filter
    :param year_range: year range
    :param value_column: which column to convert (GDP)
    :param skip_rows: skip rows until column name occurs
    :param convert_to_billion: whether to convert values to billions
    :return: pd.DataFrame
    """

    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = normalize_date(df, date_column)
    df = filter_by_year_range(df, year_column, year_range)
    if value_column and convert_to_billion:
        if column_label is None:
            raise ValueError("`column_label` must be provided when `convert_to_billion` is True.")
        df = convert_values(df, value_column, convert_to_billion=True, column_label=column_label)
    df.columns = df.columns.str.strip()
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


def preprocess_csv_type3(
        file_path, country_column, countries, year_column, year_range,
        skip_rows=None, value_column=None, convert_to_billion=False, column_label=None):
    """
    To process csv type 3, which doesn't have a column named Date, but every year as 1 column.
    :param file_path: csv file path
    :param country_column: which column to select
    :param countries: list of countries
    :param year_column: which column to select
    :param year_range: year range
    :param skip_rows: skip rows until column name occurs
    :return: pd.DataFrame
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df = filter_by_country(df, country_column, countries)
    # 自动识别年份列
    year_columns = [col for col in df.columns if col.isdigit()]  # 判断列名是否为数字
    # 转换宽表为长表
    df = pd.melt(df, id_vars=[country_column], value_vars=year_columns,
                 var_name=year_column, value_name='Value')  # 'year_column' 是动态的

    df[year_column] = pd.to_numeric(df[year_column], errors='coerce')
    df = filter_by_year_range(df, year_column, year_range)
    if value_column and convert_to_billion:
        if column_label is None:
            raise ValueError("`column_label` must be provided when `convert_to_billion` is True.")
        df = convert_values(df, value_column, convert_to_billion=True, column_label=column_label)
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
    #print(AUS_underweight)  # test success

    CHI_underweight = preprocess_csv_type2(
        file_path='data/Prevalence_of_obesity_among_adults.csv',
        country_column='Location',
        countries=['China'],
        year_column='Period',
        year_range=(2003, 2013),
        skip_rows=0
    )
    #print(CHI_underweight)  # test success

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
    print(AUS_FDI)  # test success

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
    print(CHI_FDI)  # test success

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

    AUS_gov_consume = preprocess_csv_type3(
        file_path='data/Government_consumption.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=3
    )
    #print(AUS_gov_consume)  # test success

    CHI_gov_consume = preprocess_csv_type3(
        file_path='data/Government_consumption.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=3
    )
    #print(CHI_gov_consume)  # test success

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

    AUS_tourism = preprocess_csv_type3(
        file_path='data/tourism_data.csv',
        country_column='Country Name',
        countries=['Australia'],
        year_column='Year',
        year_range=(1995, 2005),
        skip_rows=3
    )
    #print(AUS_tourism)  # test success

    CHI_tourism = preprocess_csv_type3(
        file_path='data/tourism_data.csv',
        country_column='Country Name',
        countries=['China'],
        year_column='Year',
        year_range=(2003, 2013),
        skip_rows=3
    )
    #print(CHI_tourism)  # test success

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
        year_range=(2002, 2013),
        skip_rows=2
    )
    #print(CHI_UR)  # test success





