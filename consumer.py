from kafka import KafkaConsumer
from json import loads
import pandas as pd
import joblib
import dbconfig
import sys


model = joblib.load('model/RandomForestModel.pkl')


expected_columns = model.feature_names_in_


def standardize_columns(df):
    df.columns = df.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True).str.upper()
    return df


def add_missing_columns(df, expected_columns):
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
    return df


def reorder_columns(df, expected_columns):
    return df[expected_columns]


def predict(data):
    """Random forest model"""
    if isinstance(data, str):
        data = loads(data)

    # Create a DataFrame from the data of the message
    df = pd.DataFrame([data])

    # Standardize column names
    df = standardize_columns(df)

    # Ensure the DataFrame has all the columns that the model expects
    df = add_missing_columns(df, expected_columns)

    # Reorder columns to match the expected feature order
    df = reorder_columns(df, expected_columns)

    # Predict using the loaded model
    prediction = model.predict(df)
    df['HAPPINESS_PREDICTION'] = prediction

    return df

def kafka_consumer():
    consumer = KafkaConsumer(
        'test-data',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for message in consumer:
        message_data = message.value
        print(f"Received message: {message_data}")

        try:
            df_with_prediction = predict(message_data)
            print(f"Data with prediction: {df_with_prediction}")
            dbconfig.load_data(df_with_prediction, 'Prediction')
        except ImportError as e:
            print(f"Error in prediction: {e}")


if __name__ == '__main__':
    dbconfig.create_table('Prediction')
    kafka_consumer()
