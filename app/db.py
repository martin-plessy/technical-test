import sqlite3, os
from typing import Any, Iterable


class DatabaseConnection:

    def __init__(self):
        self.conn = None

    def _reset_database(self):
        self._close()

        if os.path.exists("technical_test.db"):
            os.remove("technical_test.db")

        self._connect()

        with open("database_setup.sql", 'r') as sql_file:
            sql_string = sql_file.read()

            self._execute(sql_string, script=True)

    def _connect(self):
        self._close()

        try:
            self.conn = sqlite3.connect(r'technical_test.db')
        except sqlite3.Error as error:
            print("Unable to connect to database. Reason: " + str(error))

    def _close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    @staticmethod
    def _label_rows(rows: list, headings: list):
        response = []

        for row in rows:
            resp = {}

            for i in range(0, len(headings)):
                resp[headings[i][0]] = row[i]

            response.append(resp)

        return response

    def _execute(self, query: str, expect_return: bool = False, return_last_row_id: bool = False, return_row_count: bool = False, script: bool = False, parameters: Iterable[Any] = []):
        if self.conn is None:
            self._connect()

        attempts = 0

        while attempts < 2:
            attempts += 1

            try:
                cursor = self.conn.cursor()

                if script:
                    cursor.executescript(query)
                else:
                    cursor.execute(query, parameters)

                self.conn.commit()

                if return_last_row_id:
                    return cursor.lastrowid
                elif return_row_count:
                    return cursor.rowcount
                elif expect_return:
                    return self._label_rows(cursor.fetchall(), cursor.description)
                else:
                    return True
            except sqlite3.Error as error:
                if attempts < 2:
                    print("Query failed. Attempting to execute again")

                    self._connect()
                else:
                    print("Query failed. Reason: " + str(error))

                    return False

    def select(self, query: str, parameters: Iterable[Any] = []):
        return self._execute(query, expect_return=True, parameters=parameters)

    def insert(self, query: str, parameters: Iterable[Any] = [], expect_return: bool = False, return_last_row_id: bool = True):
        return self._execute(query, expect_return=expect_return, parameters=parameters, return_last_row_id=not expect_return and return_last_row_id)

    def update(self, query: str, parameters: Iterable[Any] = [], expect_return: bool = False, return_row_count: bool = True):
        return self._execute(query, expect_return=expect_return, parameters=parameters, return_row_count=not expect_return and return_row_count)

    def delete(self, query: str, parameters: Iterable[Any] = []):
        return self._execute(query, expect_return=False, parameters=parameters)
