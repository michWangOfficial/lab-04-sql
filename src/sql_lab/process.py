import getpass
import logging
import os

import mysql.connector
import pandas as pd


def read_data(filename):
    """
    Read a CSV file and return a DataFrame.
    """
    data = pd.read_csv(filename)
    logging.info("Read %d rows", len(data))
    return data


def clean_data(data):
    """
    Remove rows with missing values and return the cleaned DataFrame
    """
    data = data.dropna()
    logging.info("Kept %d rows after cleaning", len(data))
    return data


def load_data(data, table):
    """
    Create the mock table if needed and upload the DataFrame to MySQL.
    """
    if table != "mock":
        raise ValueError("The table name must be mock")

    connection = None
    cursor = None
    try:
        password = os.getenv("DBPASS") or os.getenv("MYSQL_PWD")
        if not password:
            password = getpass.getpass("Database password: ")
        database = os.getenv("DBNAME") or "edr2ft_mock"
        if database != "edr2ft_mock":
            logging.warning("Ignoring DBNAME=%s; using edr2ft_mock", database)
            database = "edr2ft_mock"
        connection = mysql.connector.connect(
            host=os.getenv("DBHOST") or "ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com",
            database=database,
            user=os.getenv("DBUSER") or "edr2ft",
            password=password,
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mock (
                id BIGINT PRIMARY KEY,
                `group` VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                gender VARCHAR(255),
                ip_address VARCHAR(255)
            )
        """)
        for row in data.itertuples(index=False, name=None):
            cursor.execute(
                "INSERT INTO mock VALUES (%s, %s, %s, %s, %s, %s)",
                (int(row[0]), *row[1:]),
            )
        connection.commit()
        logging.info("Uploaded %d rows", len(data))
    except mysql.connector.Error:
        if connection is not None:
            connection.rollback()
        logging.exception("Upload failed")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def main():
    """
    Read, clean, and upload the CSV data.
    """
    logging.basicConfig(level=logging.INFO)
    load_data(clean_data(read_data("MOCK_DATA.csv")), "mock")


if __name__ == "__main__":
    main()