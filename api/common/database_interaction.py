"""
database_interaction is aimed to limit code redundancy for PostgreSQL interaction.
"""

# External dependencies
import psycopg2


class DataBase:
    """
    DataBase is a class to simplify connections with the PostgreSQL database.

    Usage:
        To create a new data base connection, create it with `DataBase(connection_data)` where
        connection_data is a dictionary containing the following keys:

    Args:
        database (str): The name of the database to connect to,
        user (str): The username used to connect to the database
        password (str): The password for the respective user
        host (str): The host IP of the data base
        port (str): The connection port for the database
    """

    def __init__(self, connection_data):
        self.connection_data = connection_data

    def _connect_to_db(self):
        '''
        Returns a database connection

        Returns:
            A database connection
        '''
        return psycopg2.connect(
            database=self.connection_data['database'],
            user=self.connection_data['user'],
            password=self.connection_data['password'],
            host=self.connection_data['host'],
            port=self.connection_data['port']
        )

    def select(self, select_string):
        '''
        Returns the query results from the database for the select_string.

        Args:
            select_string (str): A string representing the database query

        Returns:
            list: A list of tuples of query results from the database
        '''
        # Establish database connection
        db = self._connect_to_db()
        # Query for restults based on the query string (select_string) and store the results
        cur = db.cursor()
        cur.execute(select_string)
        results = cur.fetchall()
        # Close the database connection
        db.close()
        return results

    def insert(self, insert_string):
        '''
        Insert data into the database

        Args:
            insert_string (str): A string representing the data to insert
        '''
        self._modify_data(insert_string)

    def update(self, update_string):
        '''
        Update data in the database

        Args:
            update_string (str): A string representing the data to update
        '''
        self._modify_data(update_string)

    def _modify_data(self, query_string):
        '''
        Modify data in the database

        Args:
            query_string (str): A string representing the data to modify
        '''
        # Establish database connection
        db = self._connect_to_db()
        # Insert the desired data into the db
        cur = db.cursor()
        cur.execute(query_string)
        db.commit()
        # Close the database connectionz
        db.close()
