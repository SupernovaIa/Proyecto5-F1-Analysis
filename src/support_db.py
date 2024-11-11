# Database Connection and Operations
# -----------------------------------------------------------------------
import psycopg2
from psycopg2 import OperationalError, errorcodes


def create_db(database_name: str = 'formula_one'):
    """
    Creates a PostgreSQL database with the provided name if it does not already exist.

    Parameters:
    - database_name (str): The name of the database to be created.
    """
    connection = None
    try:
        # Establish connection to the default 'postgres' database
        connection = psycopg2.connect(
            database='postgres',
            user='my_user',
            password='admin',
            host='localhost',
            port='5432'
        )
        connection.autocommit = True  # Ensure CREATE DATABASE runs outside of a transaction block

        with connection.cursor() as cursor:
            # Check if the database already exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
            db_exists = cursor.fetchone()

            if not db_exists:
                # Create the database if it does not exist
                cursor.execute(f"CREATE DATABASE {database_name};")
                print(f"Database {database_name} created successfully.")
            else:
                print("The database already exists.")

    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print('Incorrect password')
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print('Connection error')
        elif e.pgcode == errorcodes.INVALID_CATALOG_NAME:
            print('Database does not exist')
        else:
            print(f"Database error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Ensure connection closure
        if connection:
            try:
                connection.close()
                print("Database connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")


def table_creation(queries: list):
    """
    Creates tables in a PostgreSQL database by executing a series of SQL table creation queries.

    Parameters:
    - queries (list of str): List of SQL queries to execute, each defining a table structure.
    """
    # Set connection
    try:
        connection = psycopg2.connect(
            database='formula_one',
            user='my_user',
            password='admin',
            host='localhost',
            port='5432'
        )

        # Queries execution
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
        
        # Commit the transaction
        connection.commit()
        print("Tables created successfully.")

    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print('Incorrect password')
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print('Connection error')
        elif e.pgcode == errorcodes.INVALID_CATALOG_NAME:
            print('Database does not exist')
        else:
            print(f"Database error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Ensure connection closure
        if connection:
            connection.close()
            print("Database connection closed.")


def data_insertion(query: str, values: list):
    """
    Inserts multiple rows of data into a PostgreSQL database based on a specified query and values.

    Parameters:
    - query (str): SQL query to execute, typically an INSERT statement with placeholders for data.
    - values (list of tuple): List of tuples containing values to insert, each tuple representing a row.
    """
    # Set connection
    try:
        connection = psycopg2.connect(
            database='formula_one',
            user='my_user',
            password='admin',
            host='localhost',
            port='5432'
        )

        # Queries execution
        with connection.cursor() as cursor:
            cursor.executemany(query, values)
        
        # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")

    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print('Incorrect password')
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print('Connection error')
        elif e.pgcode == errorcodes.INVALID_CATALOG_NAME:
            print('Database does not exist')
        else:
            print(f"Database error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Ensure connection closure
        if connection:
            connection.close()
            print("Database connection closed.")


def sql_query(query: str):
    """
    Executes a given SQL query on a PostgreSQL database and retrieves all results.

    Parameters:
    - query (str): The SQL query to be executed on the database.

    Returns:
    - result (list of tuples | None): A list of tuples containing the query results if the execution is successful, or `None` if an error occurs.
    """

    # Initialize result to avoid returning undefined variable
    result = None
    connection = None
    
    try:
        # Establish the connection
        connection = psycopg2.connect(
            database='formula_one',
            user='my_user',
            password='admin',
            host='localhost',
            port='5432'
        )

        # Query execution
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        
        print("Query performed successfully.")

    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print('Incorrect password')
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print('Connection error')
        elif e.pgcode == errorcodes.INVALID_CATALOG_NAME:
            print('Database does not exist')
        else:
            print(f"Database error: {e}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        # Closing connection
        if connection:
            try:
                connection.close()
                print("Database connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")

    return result