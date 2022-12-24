import QtDatabase
import os, csv
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

@QtDatabase.hookimpl
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
        
        column_string += f"{column_name}{' TEXT'}{comma}"
    
    query_string = f"{'CREATE TABLE IF NOT EXISTS '}{table_name}" \
                    f"{' ('}{'id INTEGER PRIMARY KEY AUTOINCREMENT, '}{column_string}{')'}"
    
    # create table query
    query.exec(query_string)

@QtDatabase.hookimpl
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

@QtDatabase.hookimpl
def insert_csv(QtDatabaseObj, table_name, csv_path):
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

    return column_names

@QtDatabase.hookimpl
def insert_into_merged_timeline(QtDatabaseObj, selected_columns, merged_timeline_table):
    # create table merged-timeline
    column_name_merged_timeline = ['timestamp', 'event', 'source']
    QtDatabaseObj.create_table(merged_timeline_table, column_name_merged_timeline)

    # select for each timeline then insert to merged-timeline
    for timeline_name, column_names in selected_columns.items():
        # sort column to make sure the order: [timestamp, event]
        column_sorted = []
        for column_type, column_name in column_names.items():
            if column_type == 'timestamp':
                if len(column_sorted) > 1:
                    column_sorted.insert(0, column_name)
                else:
                    column_sorted.append(column_name)

            elif column_type == 'event':
                column_sorted.append(column_name)

        # build query string
        column_string = ''
        comma = ', '
        column_names_len = len(column_sorted)

        # column names
        for index, column_name in enumerate(column_sorted):
            if index == column_names_len - 1:
                comma = ''
            column_string += f"{column_name}{comma}"

        # select timeline table based on timeline_name
        select_query = QSqlQuery()

        # query string
        query_string = f"{'SELECT '}{column_string}{' FROM '}{timeline_name}"
        select_query.exec(query_string)

        # get data and insert
        while select_query.next():
            # row = [timestamp, event, source]
            row = [select_query.value(column_sorted[0]), select_query.value(column_sorted[1]), timeline_name]
            QtDatabaseObj.insert_data(merged_timeline_table, column_name_merged_timeline, row)