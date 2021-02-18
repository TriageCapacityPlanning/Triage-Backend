import pytest
from psycopg2 import ProgrammingError, DatabaseError
from api.common.database_interaction import DataBase


class TestDatabaseInteraction:
    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.database = DataBase({})

    def test_select_connection_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect.side_effect = DatabaseError

        with pytest.raises(DatabaseError):
            self.database.select(query_string)

    def test_select_error_query(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a bad query is passed.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().fetchall.side_effect = ProgrammingError()

        with pytest.raises(ProgrammingError):
            self.database.select(query_string)

        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().cursor().__enter__().fetchall.assert_called()
        mock_connect().__enter__().close.assert_not_called()

    def test_select_no_rows_found(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an empty list is returned if a query results with no rows
        """
        query_string = 'SELECT * FROM table;'
        expected = []
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().fetchall.return_value = expected

        assert self.database.select(query_string) == expected
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().cursor().__enter__().fetchall.assert_called()
        mock_connect().__enter__().close.assert_called()

    def test_select_singleton(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a singleton list is returned if a query results with 1 row
        """
        query_string = 'SELECT * FROM table;'
        expected = [('test1', 'test2', 'test3')]
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().fetchall.return_value = expected

        assert self.database.select(query_string) == expected
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().cursor().__enter__().fetchall.assert_called()
        mock_connect().__enter__().close.assert_called()

    def test_select_multiple_rows(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that the number of rows that the query finds has is returned by select
        """
        query_string = 'SELECT * FROM table;'
        expected = [('test1', 'test2', 'test3'), ('test1', 'test2', 'test3'), ('test1', 'test2', 'test3')]
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().fetchall.return_value = expected

        assert self.database.select(query_string) == expected
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().cursor().__enter__().fetchall.assert_called()
        mock_connect().__enter__().close.assert_called()

    def test_insert_connection_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect.side_effect = DatabaseError

        with pytest.raises(DatabaseError):
            self.database.insert(query_string)

    def test_insert_error_query(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a bad query is passed.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().execute.side_effect = ProgrammingError()

        with pytest.raises(ProgrammingError):
            self.database.insert(query_string)

        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().commit.assert_not_called()
        mock_connect().__enter__().close.assert_not_called()

    def test_insert_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests a successful insert statement.
        """
        query_string = "INSERT INTO table ('test') VALUES ('test');"
        mock_connect = mocker.patch('psycopg2.connect')

        self.database.insert(query_string)
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().commit.assert_called()
        mock_connect().__enter__().close.assert_called()

    def test_update_connection_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect.side_effect = DatabaseError

        with pytest.raises(DatabaseError):
            self.database.update(query_string)

    def test_update_error_query(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a bad query is passed.
        """
        query_string = 'bad QuEry 5$3'
        mock_connect = mocker.patch('psycopg2.connect')
        mock_connect().__enter__().cursor().__enter__().execute.side_effect = ProgrammingError()

        with pytest.raises(ProgrammingError):
            self.database.update(query_string)

        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().commit.assert_not_called()
        mock_connect().__enter__().close.assert_not_called()

    def test_update_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests a successful update statement.
        """
        query_string = "UPDATE table SET 'test'='this_will_work' WHERE table.testing = 'true';"
        mock_connect = mocker.patch('psycopg2.connect')

        self.database.update(query_string)
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with(query_string)
        mock_connect().__enter__().commit.assert_called()
        mock_connect().__enter__().close.assert_called()
