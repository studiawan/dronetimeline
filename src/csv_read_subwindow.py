from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QProgressBar,
)
from PyQt5.QtSql import QSqlQuery
import time, csv, threading, os
import sqlite3
def thread_insert_to_db_function(parent, csv_file, table_name, column_names, database_path):
    time_start = time.time()
    con = sqlite3.connect(f"{os.path.basename(database_path)}{'.db'}")
    cur = con.cursor()
    cur.execute(f"SELECT MAX(id) FROM {table_name}")

    # Check last entry of the database
    row = cur.fetchone()[0]
    last_inserted_id = int(row) if bool(row) else 0
    
    
    n = 1 # number of lines in csv
    datas = []

    # initiate progress bar value
    parent.completed = 0

    with open(csv_file) as f:
        n += sum(1 for line in f)
    with open(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=',')
        # skipping1 header
        next(csv_reader)

        # skipping last_inserted_id number of records
        for i in range(0, last_inserted_id): 
            next(csv_reader)
            parent.completed += 1/n
            parent.progress.setValue(parent.completed*100) 
            
        for row in csv_reader:
            parent.completed += 1/n
            datas.append((row))
            parent.progress.setValue(parent.completed*100)
            
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
    query_string = f"{'INSERT INTO '}{table_name}{column_string}"
    
    cur.executemany(query_string, datas)
    con.commit()
    cur.close()
    print("finished inserting from csv")

class CSVReadSubWindow(QMdiSubWindow):
    def __init__(self, csv_file, table_name, column_names, database_path):
        super().__init__()
        self.table_name = table_name
        self.csv_file = csv_file
        self.column_names = column_names
        self.database_path = database_path
        self.progress = None
        
    def show_ui(self):
        # set title and geometry
        subwindow_title = f"{'Reading Forensics timeline: '}{self.table_name}"
        self.setWindowTitle(subwindow_title)
        self.setGeometry(60, 60, 600, 400)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.resize(300, 100)
        self.show()
        threading.Thread(target=thread_insert_to_db_function, args=(self, self.csv_file, self.table_name, self.column_names, self.database_path)).start()