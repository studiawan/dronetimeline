import pluggy

hookspec = pluggy.HookspecMarker("QtDatabase")
"""Marker to be imported and used in plugins (and for own implementations)"""

@hookspec(firstresult=True)
def create_table(QtDatabaseObj, table_name, column_names):
    """Create a table in the database

    :param QtDatabaseObj: QtDatabase object
    :param table_name: name of the table
    :param column_names: list of column names
    :return: None
    """

@hookspec(firstresult=True)
def insert_data(QtDatabaseObj, table_name, column_names, row):
    """Insert data into the database

    :param QtDatabaseObj: QtDatabase object
    :param table_name: name of the table
    :param column_names: list of column names
    :param row: list of values
    :return: None
    """

@hookspec(firstresult=True)
def insert_csv(QtDatabaseObj, table_name, csv_path):
    """Insert data from a csv file into the database

    :param QtDatabaseObj: QtDatabase object
    :param table_name: name of the table
    :param csv_path: path to the csv file
    :return: list of column names
    """

@hookspec(firstresult=True)
def insert_into_merged_timeline(QtDatabaseObj, selected_columns, merged_timeline_table):
    """Insert data from the merged timeline table into the database

    :param QtDatabaseObj: QtDatabase object
    :param selected_columns: list of selected columns
    :param merged_timeline_table: name of the merged timeline table
    :return: None
    """