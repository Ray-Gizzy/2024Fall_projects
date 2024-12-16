# 2024Fall_projects
<br>

# Impacts of Hosting the Olympics: A Comparative Study of Australia, China, Canada, Greece, Spain, United Kindom, United States and South Korea
<br><br>
## Overview
This project investigates the impacts of hosting the Olympic Games through a combined analysis of **between-country differences** and **temporal trends**. Using the 1976 Montreal Olympics(Canada), 1988 Seoul Olympics(South Korea), 1992 Barcelona Olympics(Spain),1996 Atlanta Olympics(United States), 2000 Sydney Olympics (Australia), 2004 Athens Olympics(Greece) and the 2008 Beijing Olympics (China) as case studies, we analyze changes in key indicators over the 5-year periods before and after the events. These indicators include economic, tourism, health, environment, and employment.

The study aims to:
- Compare changes in key indicators over the 5-year periods before and after hosting Olympic for these countries.
- Explore how these impacts evolve over short-term (1–2 years) and middle-term (3-5 years) periods.

For data selection, we intend to use data after 1970 which means that the earliest Olympic Games should be Montreal 1976 (Canada). Meanwhile, since we aim to analyze the effect up to 5 years after the olympics, so our latest pick can be United Kingdom(2012) and Brazil(2016). Brazil's data is rough and not accurate so we decide to hold our step after acquiring the United Kingdom's data.

<br><br>
## Hypotheses

This project evaluates two dimensions of Olympic impacts:

1. Between-Country Hypotheses
- **Economic Growth**: Emerging economies like China and South Korea experience more significant short-term economic growth after hosting the Olympics, but their medium- to long-term growth may decelerate. In contrast, developed economies like Australia and Canada show more stable economic growth, with benefits likely to sustain over the medium term (3–5 years).
- **Tourism Impact**: Tourism-dependent countries like Spain and Greece see a substantial increase in international tourists during the Olympics, with the growth potentially lasting longer than in other countries.
- **Health and Environment**: Hosting the Olympics improves residents' health indicators.China implements large-scale environmental initiatives during the Olympics but faces a higher risk of returning to high emissions in the medium term. In contrast, resource-rich countries like Australia and Canada are more likely to maintain environmental improvements over the long term.
- **Labor Market Dynamics**: All countries experience a significant drop in unemployment during the Olympic preparation period (short-term) due to infrastructure projects.

2. Temporal Hypotheses
- **Short-Term Effects (1–2 years)**: Hosting the Olympics leads to short-term benefits for all countries, including reduced unemployment rates, increased GDP, FDI, and tourism, as well as improvements in environmental and health indicators due to Olympic commitmenates, increases GDP, FDI and tourism, and boosts environmental and health initiatives as part of Olympic commitments.
- **Middle-Term Effects (3-5 years)**: Developed countries like Australia, Canada, and the UK are more likely to sustain the economic, environmental, and health benefits of hosting the Olympics


<br><br>
## Methodology
We analyze data across five key dimensions:

1. Economic Indicators
- GDP: [country](data/[country]-gdp-gross-domestic-product.csv)
- Foreign Direct Investment: [Foreign Direct Investment](data/Foreign_Direct_Investment.csv)
- Government Final Consumption Expenditure: [Government Consumption](data/Government_consumption.csv)

2. Tourism Performance
- International Tourists Arrival: [Tourism](data/tourism_data.csv)

3. Health Metrics
- Obesity Prevalence: [Adult Obesity](data/Prevalence_of_obesity_among_adults.csv)
- Underweight Prevalence: [Adult Underweight](data/Prevalence_of_underweight_among_adults.csv)

4. Environmental Indicators
- Greenhouse Gas Emissions: [Greenhouse Gas Emission](data/ghg-emissions.csv)

5. Labor Market:
- Employment Change: [Unemployment Rate China](data/Unemployment_rate_China.csv), [Unemployment Rate for the rest of the country](data/Unemployment_rate.csv),


Data Sources:

Annual GDP Report: china-gdp-gross-domestic-product.csv
https://www.macrotrends.net/global-metrics/countries/CHN/china/gdp-gross-domestic-product

Foreign Direct Investment: Foreign_Direct_Investment.csv
https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD

General Government Final Consumption Expenditure: Government_consumption.csv
https://data.worldbank.org/indicator/NE.CON.GOVT.CD?end=2015&locations=CN-AU


<br><br>
Tourism Data for all country: tourism_data.csv
https://data.worldbank.org/indicator/ST.INT.ARVL?end=2015


<br><br>
Prevalence of obesity among adults: Prevalence_of_obesity_among_adults.csv
https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-obesity-among-adults-bmi--30-(crude-estimate)-(-)

Prevalence of underweight among adults: Prevalence_of_underweight_among_adults.csv
https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-underweight-among-adults-bmi-18-(crude-estimate)-(-)



<br><br>
Green House Gas Emissions: ghg-emissions.csv
https://www.kaggle.com/code/avanishsingh007/green-house-gas-historical-emission-data-analysis?select=ghg-emissions.csv



<br><br>
Urban Population %: Percentage_Urban_Population.csv
https://data.worldbank.org/topic/urban-development?locations=CN-AU


<br><br>
Unemployment Rate(world databank): Unemployment_rate_Australia.csv
https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?end=2023&locations=AU&start=1991&view=chart

China Unemployment Rate (2002-2015): Unemployment_rate_China.csv
https://data.stats.gov.cn/english/easyquery.htm?cn=C01
