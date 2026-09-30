import getpass
import logging
import os

import mysql.connector


_password = None

COUNT_QUERIES = {
    "id": "SELECT id AS category, COUNT(*) AS total FROM mock GROUP BY id ORDER BY total DESC",
    "group": "SELECT `group` AS category, COUNT(*) AS total FROM mock GROUP BY `group` ORDER BY total DESC",
    "first_name": "SELECT first_name AS category, COUNT(*) AS total FROM mock GROUP BY first_name ORDER BY total DESC",
    "last_name": "SELECT last_name AS category, COUNT(*) AS total FROM mock GROUP BY last_name ORDER BY total DESC",
    "gender": "SELECT gender AS category, COUNT(*) AS total FROM mock GROUP BY gender ORDER BY total DESC",
    "ip_address": "SELECT ip_address AS category, COUNT(*) AS total FROM mock GROUP BY ip_address ORDER BY total DESC",
}


def connect():
    """
    Connect to the lab's mock database.
    """
    global _password
    if _password is None:
        _password = os.getenv("DBPASS") or os.getenv("MYSQL_PWD") or getpass.getpass("Database password: ")
    database = os.getenv("DBNAME") or "edr2ft_mock"
    if database != "edr2ft_mock":
        raise ValueError("DBNAME must be edr2ft_mock for Case Study 2")
    connection = mysql.connector.connect(
        host=os.getenv("DBHOST") or "ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com",
        database=database,
        user=os.getenv("DBUSER") or "edr2ft",
        password=_password,
    )
    logging.info("Connected to %s", database)
    return connection


def fetch(query, parameters=()):
    """
    Run a SELECT query and return its rows.
    """
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, parameters)
        rows = cursor.fetchall()
        logging.info("Fetched %d rows", len(rows))
        return rows
    except mysql.connector.Error:
        logging.exception("Query failed")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_data_by_group(value):
    """
    Return all mock rows whose group equals value.
    """
    rows = fetch("SELECT * FROM mock WHERE `group` = %s", (value,))
    logging.info("Found %d rows for group %s", len(rows), value)
    return rows


def plot_counts(groupby):
    """
    Return the number of mock rows for each value of a column.
    """
    if groupby not in COUNT_QUERIES:
        raise ValueError("Unknown column: " + groupby)
    rows = fetch(COUNT_QUERIES[groupby])
    logging.info("Counted %d distinct %s values", len(rows), groupby)
    return rows


def main():
    """
    Display sample rows for one group and counts by group
    """
    logging.basicConfig(level=logging.INFO)
    matches = get_data_by_group("item1")
    print("Rows in item1:", len(matches))
    for row in matches[:5]:
        print(row)
    for row in plot_counts("group"):
        print(row)


if __name__ == "__main__":
    main()
