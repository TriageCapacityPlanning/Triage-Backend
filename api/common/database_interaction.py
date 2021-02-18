"""
database_interaction is aimed to limit code redundancy for PostgreSQL.
"""

# External dependencies
import psycopg2


class DataBase:
    """
    DataBase is a class to simplify connections with the PostgreSQL database.

    Usage:
        To create a new data base connection, create it with
        `DataBase(connection_data)` where connection_data is a dictionary
        containing the following keys:

    Args:
        database (str): The name of the database to connect to,
        user (str): The username used to connect to the database
        password (str): The password for the respective user
        host (str): The host IP of the data base
        port (str): The connection port for the database
    """

    def __init__(self, connection_data):
        self.connection_data = connection_data

    def select(self, select_string):
        """
        Returns the query results from the database for the select_string.

        Args:
            select_string (str): A string representing the database query

        Returns:
            list: A list of tuples of query results from the database
        """
        # Establish database connection
        with psycopg2.connect(**self.connection_data) as db:
            # Establish a cursor to interact with the database
            with db.cursor() as cur:
                # Query for restults based on the query string (select_string)
                cur.execute(select_string)
                # Store the results
                results = cur.fetchall()
        # Close the database connection
        db.close()
        return results

    def insert(self, insert_string):
        """
        Insert data into the database

        Args:
            insert_string (str): A string representing the data to insert
        """
        self._modify_data(insert_string)

    def update(self, update_string):
        """
        Update data in the database

        Args:
            update_string (str): A string representing the data to update
        """
        self._modify_data(update_string)

    def _modify_data(self, query_string):
        """
        Modify data in the database

        Args:
            query_string (str): A string representing the data to modify
        """
        # Establish database connection
        with psycopg2.connect(**self.connection_data) as db:
            # Establish a cursor to interact with the database
            with db.cursor() as cur:
                # Insert the desired data into the db
                cur.execute(query_string)
                db.commit()
        # Close the database connection
        db.close()

    def insert_data_stream_of_tuples(self, table, data_attributes, data_stream):
        """
        Insert a large amount of data into the database

        Args:
            table (str): The table to insert the data into
            data_attributes (tuple, str): A tuple representing which data attributes the data_stream tuples have
            data_stream (list, tuples, str): A list of tuples that represent the data that will be inserted
        """
        raise NotImplementedError()
