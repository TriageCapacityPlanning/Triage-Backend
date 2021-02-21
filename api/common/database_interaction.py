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

    def insert(self, insert_string, returning=False):
        """
        Insert data into the database

        Args:
            insert_string (str): A string representing the data to insert
        """
        return self._modify_data(insert_string, returning)

    def update(self, update_string, returning=False):
        """
        Update data in the database

        Args:
            update_string (str): A string representing the data to update
        """
        return self._modify_data(update_string, returning)

    def _modify_data(self, query_string, returning=False):
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
                if returning:
                    val = cur.fetchone()[0]
        # Close the database connection
        db.close()
        if returning:
            return val

    def insert_data_from_file(self, table, data_column_order, data_file, seperator):
        """
        Insert a large amount of data into the database from a file

        Args:
            table (str): The table to insert the data into
            data_header_order (tuple, str): A tuple representing which data attributes the data_file tuples have
            data_file (file): A file with the data to upload to the database
            seperator (str): the file character seperators
        """
        # Establish database connection
        with psycopg2.connect(**self.connection_data) as db:
            # Establish a cursor to interact with the database
            with db.cursor() as cur:
                cur.copy_from(data_file, table, sep=seperator, columns=data_column_order)
        db.close()
