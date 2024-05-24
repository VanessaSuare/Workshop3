from kafka import KafkaConsumer
from json import loads
import pandas as pd
import joblib
import dbconfig


model = joblib.load('model/RandomForestModel.pkl')


def predict(data):
    """Predict model function"""
    if isinstance(data, str):
        data = loads(data)

    df = pd.DataFrame([data])

    prediction = model.predict(df.drop(columns=['happiness_score'], axis=1, errors='ignore'))
    df['prediction'] = prediction

    return df


def kafka_consumer():
    """kafka consumer function"""
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
