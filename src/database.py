import sqlite3
import os
import csv
from collections import OrderedDict


class Database:
    def __init__(self, database_name, database_path):
        self.database_name = database_name + '.db'
        self.database_path = database_path
        self.connection = self.connect()

    def connect(self):
        try:
            connection = sqlite3.connect(os.path.join(self.database_path, self.database_name))
            print('Database connection is successful.')
            return connection

        except sqlite3.Error as e:
            print(e)

    def close_connection(self):
        self.connection.close()

    def select(self, table_name):
        select_query = f'SELECT * FROM {table_name}'
        results = self.connection.execute(select_query)
        for row in results:
            print(row)

    def create_table(self, table_name, columns):
        # build dictionary column name and its type
        table = OrderedDict()
        table['id'] = 'INTEGER PRIMARY KEY'
        for column in columns:
            table[column] = 'TEXT'

        # column names formatting
        fieldset = []
        for col, definition in table.items():
            fieldset.append("{0} {1}".format(col, definition))
        fieldset = tuple(fieldset)

        # create query
        create_query = f'CREATE TABLE IF NOT EXISTS {table_name} {fieldset}'
        self.connection.execute(create_query)

    def insert(self, table_name, csv_file):
        # read each row in csv file then insert
        line_count = 0
        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                # get column names and create table
                if line_count == 0:
                    columns = tuple(row)
                    self.create_table(table_name, columns)

                # insert data
                else:
                    values = tuple(row)
                    insert_query = f'INSERT INTO {table_name} {columns} VALUES {values}'
                    self.connection.execute(insert_query)

                line_count += 1
