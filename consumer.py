from kafka import KafkaConsumer
from json import loads
import pandas as pd
import joblib
import config

model = joblib.load('model/randomForest.pkl')

def standardize_columns(df):
    df.columns = df.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True).str.lower()
    return df

def predict(data):
    # Ensure the data is a dictionary
    if isinstance(data, str):
        data = loads(data)
        
    # Create a DataFrame from the data of the message
    df = pd.DataFrame([data])

    # Standardize column names
    df = standardize_columns(df)

    # Predict using the loaded model
    prediction = model.predict(df.drop(columns=['happiness_score'], axis=1, errors='ignore'))
    df['prediction'] = prediction

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
            db.load_data(df_with_prediction, 'happiness_predictions')
        except Exception as e:
            print(f"Error in prediction: {e}")

if __name__ == '__main__':
    db.create_table('happiness_predictions')
    kafka_consumer()