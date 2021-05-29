import csv
from sqlalchemy import create_engine, Column, Table, MetaData, select
from sqlalchemy import String, Integer


class Database:
    def __init__(self, database_name, database_path):
        self.database_path = database_path
        db_uri = f'sqlite:///{database_name}.db'
        engine = create_engine(db_uri, echo=True)
        self.connection = engine.connect()
        self.meta = MetaData(engine)

    def create_table(self, table_name, columns):
        # columns and table definition
        column_definition = list()
        column_definition.append(Column('id', Integer, primary_key=True))
        for column_name in columns:
            column_definition.append(Column(column_name, String))

        table = Table(table_name, self.meta, *column_definition, sqlite_autoincrement=True)
        self.meta.create_all()

        return table

    def insert(self, table_name, csv_file):
        # read each row in csv file then insert
        line_count = 0
        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                # get column names and create table
                if line_count == 0:
                    column_names = row
                    table = self.create_table(table_name, row)

                # insert data
                else:
                    # get data
                    data = {}
                    index = 0
                    for column_name in column_names:
                        data[column_name] = row[index]
                        index += 1

                    # insert
                    insert = table.insert().values(data)
                    self.connection.execute(insert)

                line_count += 1

        self.select(table)

    def select(self, table):
        select_query = table.select()
        results = self.connection.execute(select_query)

        for row in results:
            print(row)
