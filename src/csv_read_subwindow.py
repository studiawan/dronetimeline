
from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QProgressBar,
)

import sqlite3, time, os, csv
from EntityRecognition import EntityRecognition


class CSVReadSubWindow(QMdiSubWindow):
    def __init__(self, csv_file, table_name, column_names, database_path):
        super().__init__()
        self.table_name = table_name
        self.csv_file = csv_file
        self.column_names = column_names
        self.database_path = database_path
        self.progress = None
        self.completed = 0
    
    # Custome function using sqlite3 to import csv  
    def insert_csv_to_db(self, parent, csv_file, table_name, column_names, database_path):
       
        write = open (table_name + '_IOB.txt', 'w')
        time_start = time.time()
        con = sqlite3.connect(f"{os.path.basename(database_path)}{'.db'}")
        cur = con.cursor()

        # Check last entry of the database
        cur.execute(f"SELECT MAX(id) FROM {table_name}")
        row = cur.fetchone()[0]
        last_inserted_id = int(row) if bool(row) else 0

        n = 1 # number of lines in csv
        datas = [] # list of datas that will go into sqlite
        entity_recogntion = EntityRecognition()
        with open(csv_file) as f:
            n += sum(1 for line in f)

        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            # skipping header
            next(csv_reader)

            # skipping last_inserted_id number of records
            for i in range(0, last_inserted_id): 
                next(csv_reader)
                self.completed += 1/n
                self.progress.setValue(self.completed*100) 


            for row in csv_reader:
                # find message and event column index
                index_message = column_names.index('message')
                index_event = column_names.index('event')

                # Do entity recognition
                row[index_event], doc, entities = entity_recogntion.find_entity(row[index_event])
                row[index_message], doc , entities = entity_recogntion.find_entity(row[index_message])
                datas.append((row))

                # IOB.txt Generator
                hasil = entity_recogntion.IOB_formater(doc, entities)
                for x in hasil :
                    write.write(str(x[0]) + " " + str(x[1]) + '\n')
                write.write('\n')

                self.completed += 1/n
                self.progress.setValue(self.completed*100)

        write.close()

        column_string = ''
        comma = ', '
        column_names_len = len(column_names)

        # column names
        for index, column_name in enumerate(column_names):
            if index == column_names_len - 1:
                comma = ''
            column_string += f"{column_name}{comma}"
        column_string = f"{'('}{column_string}{')'}{' VALUES '}"
        self.progress.setValue(95)
        
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
        
        # every datas that have been inserted to <list>datas will be inserted in one process
        cur.executemany(query_string, datas)
        con.commit()
        cur.close()
        print("finished inserting from csv")
        self.progress.setValue(100)

        parent.signal_receiver.emit(table_name, column_names)

    def show_ui(self):
        # set title and geometry
        subwindow_title = f"{'Reading Forensics timeline: '}{self.table_name}"
        self.setWindowTitle(subwindow_title)
        self.setGeometry(60, 60, 600, 400)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.resize(300, 100)
        self.show()