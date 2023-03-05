import pluggy
import os

from QtDatabase import hookspecs, lib
from PyQt5.QtSql import QSqlDatabase

class QtDatabase:
    def __init__(self, database_path):
        self.pm = pluggy.PluginManager("QtDatabase")
        self.pm.add_hookspecs(hookspecs)
        self.pm.load_setuptools_entrypoints("QtDatabase")
        self.pm.register(lib)

        self.database_name = f"{database_path}{'.db'}"
        self.connection = QSqlDatabase.addDatabase('QSQLITE')
        self.connection.setDatabaseName(self.database_name)

    def create_table(self, table_name, column_names):
        """Create a table in the database

        :param table_name: name of the table
        :param column_names: list of column names
        :return: None
        """
        return self.pm.hook.create_table(QtDatabaseObj=self, table_name=table_name, column_names=column_names)
    
    def insert_data(self, table_name, column_names, row):
        """Insert data into the database

        :param table_name: name of the table
        :param column_names: list of column names
        :param row: list of values
        :return: None
        """
        return self.pm.hook.insert_data(QtDatabaseObj=self, table_name=table_name, column_names=column_names, row=row)
    
    def insert_csv(self, table_name, csv_path):
        """Insert data from a csv file into the database

        :param table_name: name of the table
        :param csv_path: path to the csv file
        :return: None
        """
        return self.pm.hook.insert_csv(QtDatabaseObj=self, table_name=table_name, csv_path=csv_path)
    
    def insert_into_merged_timeline(self, selected_columns, merged_timeline_table):
        """Insert data from the merged timeline table into the database

        :param selected_columns: list of selected columns
        :param merged_timeline_table: name of the merged timeline table
        :return: None
        """
        return self.pm.hook.insert_into_merged_timeline(QtDatabaseObj=self, selected_columns=selected_columns, merged_timeline_table=merged_timeline_table)

def main():
    pass