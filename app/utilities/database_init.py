import psycopg2
from psycopg2 import sql
import pandas as pd

db_config = {
    'dbname': 'taxi_trip_data',
    'user': 'postgres',
    'password': 'Mohsin@123',
    'host': 'localhost',
    'port': 5432
}

def create_postgresql_user(username, password):
    conn = psycopg2.connect(dbname='postgres', user=db_config['user'], password=db_config['password'], host=db_config['host'], port=db_config['port'])
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (username,))
    user_exists = cursor.fetchone()

    if not user_exists:
        # Create the user
        cursor.execute(sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s").format(sql.Identifier(username)), [password])
        print(f"User '{username}' created successfully.")
    else:
        print(f"User '{username}' already exists.")

    cursor.close()
    conn.close()

def create_database_if_not_exists():
    conn = psycopg2.connect(dbname='postgres', user=db_config['user'], password=db_config['password'], host=db_config['host'], port=db_config['port'])
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_config['dbname'],))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_config['dbname'])))
        print(f"Database '{db_config['dbname']}' created.")
    else:
        print(f"Database '{db_config['dbname']}' already exists.")

    cursor.close()
    conn.close()

def create_table():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS trips (
        id SERIAL PRIMARY KEY,
        vendor_id INT,
        pickup_datetime TIMESTAMP,
        dropoff_datetime TIMESTAMP,
        passenger_count INT,
        pickup_longitude DOUBLE PRECISION,
        pickup_latitude DOUBLE PRECISION,
        dropoff_longitude DOUBLE PRECISION,
        dropoff_latitude DOUBLE PRECISION,
        store_and_fwd_flag CHAR(1),
        trip_duration INT
    );
    """

    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'trips' created or already exists.")

    cursor.close()
    conn.close()

def preprocess_data(data):
    data = data.dropna()
    numeric_columns = ['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude',
                       'dropoff_longitude', 'dropoff_latitude', 'trip_duration']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data = data[data['trip_duration'] > 0]
    print("Data preprocessing completed.")
    return data

def load_csv_to_database(csv_file):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    data = pd.read_csv(csv_file)
    data = preprocess_data(data)
    for index, row in data.iterrows():
        cursor.execute(
            """
            INSERT INTO trips (
                vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
                pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
                store_and_fwd_flag, trip_duration
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row['vendor_id'], row['pickup_datetime'], row['dropoff_datetime'], row['passenger_count'],
                row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'], row['dropoff_latitude'],
                row['store_and_fwd_flag'], row['trip_duration']
            )
        )

    conn.commit()
    print("CSV data loaded into the 'trips' table.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    csv_file_path = "your_csv_file_path.csv"

    create_database_if_not_exists()
    create_table()
    load_csv_to_database(csv_file_path)
