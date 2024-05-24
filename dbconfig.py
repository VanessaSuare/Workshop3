import pandas as pd
from sqlalchemy import create_engine, inspect, text
from configparser import ConfigParser

def load_config(filename="config/database.ini", section="postgresql"):
    """Load configuration from .ini file"""
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
        print("Configuration file loaded successfully.")
        return config
    else:
        print("Section not found%s", section)
        return None

config = load_config()

# Assemble the DATABASE_URI from the config details
user = config.get('user')
password = config.get('password')
host = config.get('host')
dbname = config.get('dbname')
port = config.get('port')
DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Create the database engine
db_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}/{config['dbname']}"
engine = create_engine(db_url)

def create_table(table_name):
    """Create table to db"""
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        df = pd.DataFrame({
            'HAPPINESS_RANK': pd.Series(dtype='float'),
            'ECONOMY_GDP_PER_CAPITA_': pd.Series(dtype='float'),
            'HEALTH_LIFE_EXPECTANCY_': pd.Series(dtype='float'),
            'FREEDOM': pd.Series(dtype='float'),
            'TRUST_GOVERNMENT_CORRUPTION_': pd.Series(dtype='float'),
            'GENEROSITY': pd.Series(dtype='float'),
            'SOCIAL_SUPPORT': pd.Series(dtype='float'),
            'YEAR': pd.Series(dtype='float'),
            'CONTINENT_ASIA': pd.Series(dtype='int64'),
            'CONTINENT_EUROPE': pd.Series(dtype='int64'),
            'CONTINENT_NORTH_AMERICA': pd.Series(dtype='int64'),
            'CONTINENT_OCEANIA': pd.Series(dtype='int64'),
            'CONTINENT_SOUTH_AMERICA': pd.Series(dtype='int64'),
            'HAPPINESS_PREDICTION': pd.Series(dtype='float')
        })
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        # Verify table creation
        if inspector.has_table(table_name):
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Failed to create table '{table_name}'.")
    else:
        print(f"Table '{table_name}' already exists.")

def load_data(df, table_name):
    """Load data to db"""
    print(f"Attempting to load data into table '{table_name}'")
    print("DataFrame columns:", df.columns.tolist())
    
    inspector = inspect(engine)
    columns_in_table = [col['name'] for col in inspector.get_columns(table_name)]
    print(f"Columns in table '{table_name}':", columns_in_table)
    
    with engine.begin() as connection:
        df.to_sql(table_name, con=connection, if_exists='append', index=False)
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5")).fetchall()
        print(f"Data in table '{table_name}':", result)
        if not result:
            print("No data found in the table after insertion.")
        else:
            print("Data loaded successfully.")