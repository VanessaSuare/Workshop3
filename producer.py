from kafka import KafkaProducer
from json import dumps
import pandas as pd
from time import sleep
import datetime as dt
import sys
import six

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from utilitys import select_features


def data_test():
    test = pd.read_csv("notebooks/data/x_test.csv")
    print("Columns in the test dataset:", test.columns.tolist())
    test = select_features(test)
    print("Columns after selecting features:", test.columns.tolist())

    y_test = pd.read_csv("notebooks/data/y_test.csv")
    print("Columns in y_test:", y_test.columns.tolist())
    test['HAPPINESS_SCORE'] = y_test['HAPPINESS_SCORE']

    return test


def kafka_producer(df_test):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092']
    )

    for i in range(len(df_test)):
        row_json = df_test.iloc[i].to_json()
        producer.send('test-data', value=row_json)
        print(f"Message sent at {dt.datetime.utcnow()}")
        sleep(2)

    print("The rows were sent successfully!")


if __name__ == '__main__':
    df_test = data_test()
    kafka_producer(df_test)
