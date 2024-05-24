import pandas as pd
from sqlalchemy import create_engine, inspect
import json


def load_config():
    """load config function"""
    try:
        with open('config/database.json', 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {}


config = load_config()

user = config.get('user')
password = config.get('password')
host = config.get('host')
dbname = config.get('dbname')
port = config.get('port')
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(DATABASE_URL)


def create_table(table_name):
    """Create table to db"""
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        df = pd.DataFrame({
            'ECONOMY_GDP_PER_CAPITA_': pd.Series(dtype='float'),
            'HEALTH_LIFE_EXPECTANCY_': pd.Series(dtype='float'),
            'FREEDOM': pd.Series(dtype='float'),
            'TRUST_GOVERNMENT_CORRUPTION_': pd.Series(dtype='float'),
            'GENEROSITY': pd.Series(dtype='float'),
            'SOCIAL_SUPPORT': pd.Series(dtype='float'),
            'CONTINENT_ASIA': pd.Series(dtype='int64'),
            'CONTINENT_EUROPE': pd.Series(dtype='int64'),
            'CONTINENT_NORTH_AMERICA': pd.Series(dtype='int64'),
            'CONTINENT_OCEANIA': pd.Series(dtype='int64'),
            'CONTINENT_SOUTH_AMERICA': pd.Series(dtype='int64'),
            'HAPPINESS_SCORE': pd.Series(dtype='float'),
            'HAPPINESS_PREDICTION': pd.Series(dtype='float')
        })
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    else:
        print(f"Table '{table_name}' already exists.")


def load_data(df, table_name):
    """Load data to db"""
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
