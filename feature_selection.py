""""""
import pandas as pd


def select_features(df):
    #df = df.drop(columns=['ECONOMY_GDP_PER_CAPITA_', 'HEALTH_LIFE_EXPECTANCY_', 'FREEDOM', 'SOCIAL_SUPPORT', 'TRUST_GOVERNMENT_CORRUPTION_', 'CONTINENT_EUROPE', 'CONTINENT_ASIA', 'CONTINENT_NORTH_AMERICA', 'CONTINENT_OCEANIA', 'CONTINENT_SOUTH_AMERICA'], axis=1)
    df = df.drop(columns=['HAPPINESS_RANK', 'GENEROSITY', 'YEAR'], axis=1)
    return df


def continent(df):
    df.columns = df.columns.str.replace(r'[^A-Za-z0-9]+', '_', regex=True).str.upper()
    df = pd.get_dummies(df, columns=['Continent'], drop_first=True)
    df = df.drop(columns=['Country or region'])
    df.replace({False: 0, True: 1}, inplace=True)
    return df
