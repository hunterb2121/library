import sqlite3


# Function to connect to the database
def create_connection():
    return sqlite3.connect("library.db")


# Function to execute a query
def execute_query(query, parameters=None):
    connection = create_connection()
    cursor = connection.cursor()

    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)

    connection.commit()
    connection.close()


# Function to fetch all results 
def fetch_all(query, parameters=None):
    connection = create_connection()
    cursor = connection.cursor()

    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    connection.close()

    if len(results) == 0:
        return None
    else:
        return results


# Function to fetch one result
def fetch_one(query, parameters=None):
    connection = create_connection()
    cursor = connection.cursor()

    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)

    results = cursor.fetchone()
    connection.close()

    if results is None:
        return None
    else:
        return results
