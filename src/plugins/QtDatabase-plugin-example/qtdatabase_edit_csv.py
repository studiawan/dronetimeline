import QtDatabase
import os, csv
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

@QtDatabase.hookimpl(tryfirst=True)
def insert_csv(QtDatabaseObj, table_name, csv_path):
    print("insert_csv from pluggin")
    with open(csv_path) as f:
        csv_reader = csv.reader(f, delimiter=',')

        line_count = 0
        for row in csv_reader:
            # get column names and create table
            if line_count == 0:
                column_names = row
                QtDatabaseObj.create_table(table_name, column_names)
                line_count += 1

            # insert data
            else:
                QtDatabaseObj.insert_data(table_name, column_names, row)
    # Modify column names
    column_names = [f"{column_name}{'_plugin'}" for column_name in column_names]
    return column_names

@QtDatabase.hookimpl(tryfirst=True)
def create_table(QtDatabaseObj, table_name, column_names):
    if not QtDatabaseObj.connection.open():
        print("Database Error: %s" % QtDatabaseObj.connection.lastError().databaseText())
    
    query = QSqlQuery()
    
    # build query string
    column_string = ''
    comma = ', '
    column_names_len = len(column_names)
    for index, column_name in enumerate(column_names):
        if index == column_names_len - 1:
            comma = ''
        
        column_name = f"{column_name}{'_plugin'}"
        column_string += f"{column_name}{' TEXT'}{comma}"
    
    query_string = f"{'CREATE TABLE IF NOT EXISTS '}{table_name}" \
                    f"{' ('}{'id INTEGER PRIMARY KEY AUTOINCREMENT, '}{column_string}{')'}"
    
    # create table query
    query.exec(query_string)
    return True

@QtDatabase.hookimpl(tryfirst=True)
def insert_data(table_name, column_names, row):
    insert_query = QSqlQuery()
    
    # build query string
    column_string = ''
    comma = ', '
    column_names_len = len(column_names)
    
    # column names
    for index, column_name in enumerate(column_names):
        if index == column_names_len - 1:
            comma = ''
        
        column_name = f"{column_name}{'_plugin'}"
        column_string += f"{column_name}{comma}"
    column_string = f"{'('}{column_string}{')'}{' VALUES '}"
    
    # values
    comma = ', '
    values_string = ''
    for index in range(column_names_len):
        if index == column_names_len - 1:
            comma = ''
        values_string += f"{'?'}{comma}"
    values_string = f"{'('}{values_string}{')'}"
    column_string += f"{values_string}"
    
    # insert data query
    insert_query.prepare(f"{'INSERT INTO '}{table_name}{' '}{column_string}")
    
    # bind data
    for value in row:
        insert_query.addBindValue(value)
    
    # insert data
    insert_query.exec()
    return True