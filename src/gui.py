import sys
import os
import re
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea,
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QComboBox,
    QListWidget,
    QPushButton,
    QLabel
)
from PyQt5.QtGui import QMouseEvent
from collections import defaultdict
from PyQt5.QtSql import QSqlTableModel
from qtdatabase import QtDatabase


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timeline_names = []
        self.case_name = ''
        self.case_directory = ''
        self.database = None
        self.model = None
        self.merged_timeline_model = None
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.timeline_list = None
        self.timeline_combo = None
        self.column_list = None
        self.final_column = None
        self.timeline_columns = {}
        self.timeline_data = {}
        self.current_table_name = ''
        self.merged_timeline_table_name = 'mergedtimeline'
        self.init_ui()

    def init_ui(self):
        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(self.newcase_action())
        file_menu.addAction(self.import_action())
        file_menu.addAction(self.exit_action())

        timeline_menu = menubar.addMenu('&Timeline')
        timeline_menu.addAction(self.merge_action())
        timeline_menu.addAction(self.show_merged_timeline_action())

        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('DroneTimeline: Forensic Timeline Analysis for Drones')
        self.show()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print('window is pressed.', self.windowTitle())

    def newcase_action(self):
        newcase_act = QAction('&Select Case Directory', self)
        newcase_act.setShortcut('Ctrl+N')
        newcase_act.setStatusTip('Select case directory')
        newcase_act.triggered.connect(self.open_directory_dialog)

        return newcase_act

    def import_action(self):
        import_act = QAction('&Import Timeline', self)
        import_act.setShortcut('Ctrl+I')
        import_act.setStatusTip('Import timeline')
        import_act.triggered.connect(self.open_file_dialog)

        return import_act

    def exit_action(self):
        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        if self.database is not None:
            self.database.connection.close()

        return exit_act

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        # get database name and database directory
        database_name = os.path.basename(directory)
        if database_name != '' and directory != '':
            self.database = QtDatabase(directory)

            # at the moment, case name == database name
            self.case_name = database_name
            self.case_directory = directory

            message = f'{"Case directory is selected: "}{directory}'
            self.show_info_messagebox(message)

    def open_file_dialog(self):
        if self.case_name == '':
            self.show_info_messagebox("Please select case directory before importing a timeline.")

        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All Files (*)",
                                                       options=options)
            if file_name:
                print(file_name)

                # insert timeline to database
                table_name = os.path.basename(file_name)
                table_name = os.path.splitext(table_name)[0]

                # make sure table name is alphanumeric
                table_name = re.sub('[\W_]+', '', table_name)

                # insert csv file to database
                column_names = self.database.insert_csv(table_name, file_name)
                self.timeline_names.append(table_name)
                self.current_table_name = table_name

                # save timeline and its column names
                self.timeline_columns[table_name] = column_names

                # show timeline in an MDI window
                self.timeline_window_trigger(table_name)
                message = f'{"Timeline is imported successfully: "}{table_name}{"."}'
                self.show_info_messagebox(message)

    def timeline_window_trigger(self, table_name):
        # define sub window
        subwindow = QMdiSubWindow()
        subwindow_title = f"{'Drone Timeline: '}{table_name}"
        subwindow.setWindowTitle(subwindow_title)
        subwindow.setGeometry(60, 60, 600, 400)

        # construct the top level widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # define widget
        search = QLineEdit()
        table = QTableView()
        self.merged_timeline_model = QSqlTableModel(db=self.database.connection)
        table.setModel(self.merged_timeline_model)
        self.merged_timeline_model.setTable(self.merged_timeline_table_name)
        self.merged_timeline_model.select()
        search.textChanged.connect(self.update_filter_merged_timeline)

        # add widget
        layout.addWidget(search)
        layout.addWidget(table)
        widget.setLayout(layout)

        # set widget
        subwindow.setWidget(widget)

        # add subwindow and show
        self.mdi.addSubWindow(subwindow)
        subwindow.show()

    def update_filter(self, s):
        filter_str = 'message LIKE "%{}%"'.format(s)
        self.model.setFilter(filter_str)

    def update_filter_merged_timeline(self, s):
        filter_str = 'message LIKE "%{}%"'.format(s)
        self.merged_timeline_model.setFilter(filter_str)

    def merge_action(self):
        newcase_act = QAction('&Merge Timelines', self)
        newcase_act.setShortcut('Ctrl+M')
        newcase_act.setStatusTip('Merge timelines')
        newcase_act.triggered.connect(self.merge_window_trigger)

        return newcase_act

    def show_merged_timeline_action(self):
        show_merged_timeline_act = QAction('S&how Merged Timeline', self)
        show_merged_timeline_act.setShortcut('Ctrl+H')
        show_merged_timeline_act.setStatusTip('Show merged timeline')
        show_merged_timeline_act.triggered.connect(self.merged_timeline_window_trigger)

        return show_merged_timeline_act

    def merge_window_trigger(self):
        # create sub window
        sub = QMdiSubWindow()
        sub.setWindowTitle("Merge Timelines")

        # construct the top level widget and layout
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        # define widget for layout1
        # label
        timeline_label = QLabel()
        timeline_label.setText('Timeline:')

        # timeline combo box
        self.timeline_combo = QComboBox()
        for timeline_name in self.timeline_names:
            self.timeline_combo.addItem(timeline_name)

        # add timeline button
        add_timeline_button = QPushButton(self)
        add_timeline_button.setText('Add timeline')
        add_timeline_button.clicked.connect(self.add_timeline_button_clicked)

        # label
        added_timeline_label = QLabel()
        added_timeline_label.setText('Added timeline:')

        # timeline list
        self.timeline_list = QListWidget()
        self.timeline_list.itemClicked.connect(self.timeline_list_clicked)

        # add widget to layout 1
        layout1.addWidget(timeline_label)
        layout1.addWidget(self.timeline_combo)
        layout1.addWidget(add_timeline_button)
        layout1.addWidget(added_timeline_label)
        layout1.addWidget(self.timeline_list)

        # add widget to layout 2
        # label
        column_label = QLabel()
        column_label.setText('Columns in selected timeline:')

        # column list
        self.column_list = QListWidget()

        # add column as timestamp
        add_column_as_timestamp_button = QPushButton()
        add_column_as_timestamp_button.setText('Add column as timestamp')
        add_column_as_timestamp_button.clicked.connect(self.add_column_as_timestamp_button_clicked)

        # add column as event button
        add_column_as_event_button = QPushButton()
        add_column_as_event_button.setText('Add column as event')
        add_column_as_event_button.clicked.connect(self.add_column_as_event_button_clicked)

        # add widgets to layout 2
        layout2.addWidget(column_label)
        layout2.addWidget(self.column_list)
        layout2.addWidget(add_column_as_timestamp_button)
        layout2.addWidget(add_column_as_event_button)

        # add widget to layout 3
        # label
        final_column_label = QLabel()
        final_column_label.setText('Added columns for timeline merging:')

        # added column list
        self.final_column = QListWidget()

        # remove column button
        remove_column_button = QPushButton()
        remove_column_button.setText('Remove column')
        remove_column_button.clicked.connect(self.remove_column_button_clicked)

        # merge timeline button
        merge_button = QPushButton()
        merge_button.setText('Merge timeline')
        merge_button.clicked.connect(self.merge_button_clicked)

        # add widgets to layout 3
        layout3.addWidget(final_column_label)
        layout3.addWidget(self.final_column)
        layout3.addWidget(remove_column_button)
        layout3.addWidget(merge_button)

        # main layout and main widget
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(layout3)
        main_widget.setLayout(main_layout)

        # add subwindow and show
        sub.setWidget(main_widget)
        self.mdi.addSubWindow(sub)
        sub.show()

    def merged_timeline_window_trigger(self):
        # define sub window
        subwindow = QMdiSubWindow()
        subwindow.setWindowTitle("Drone Timeline")
        subwindow.setGeometry(60, 60, 600, 400)

        # construct the top level widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # define widget
        search = QLineEdit()
        table = QTableView()

        # access the table in database
        self.model = QSqlTableModel(db=self.database.connection)
        table.setModel(self.model)
        self.model.setTable(self.merged_timeline_table_name)
        self.model.select()
        search.textChanged.connect(self.update_filter)

        # add widget
        layout.addWidget(search)
        layout.addWidget(table)
        widget.setLayout(layout)

        # set widget
        subwindow.setWidget(widget)

        # add subwindow and show
        self.mdi.addSubWindow(subwindow)
        subwindow.show()

    def add_timeline_button_clicked(self):
        timeline_combo_count = self.timeline_combo.count()

        # check whether combo is not empty
        if timeline_combo_count > 0:
            timeline_list_count = self.timeline_list.count()

            # check whether list is not empty
            if timeline_list_count > 0:
                is_exist = False

                # check a timeline name is exist in the list or not
                for index in range(timeline_list_count):
                    if self.timeline_combo.currentText() == self.timeline_list.item(index).text():
                        is_exist = True
                        break

                # add timeline to list if not exist
                if is_exist is False:
                    self.timeline_list.addItem(self.timeline_combo.currentText())

            # if list is empty, add item
            else:
                self.timeline_list.addItem(self.timeline_combo.currentText())

    def add_column_as_timestamp_button_clicked(self):
        self.add_column_clicked('timestamp')

    def add_column_as_event_button_clicked(self):
        self.add_column_clicked('event')

    def add_column_clicked(self, column_type):
        column_count = self.column_list.count()

        # check whether column list is not empty
        if column_count > 0 and len(self.column_list.selectedItems()) > 0:
            final_column_count = self.final_column.count()
            column_current_item = f'{self.timeline_list.currentItem().text()}{"["}{column_type}{"]: "}' \
                                  f'{self.column_list.currentItem().text()}'

            # check whether final column list is not empty
            if final_column_count > 0:
                is_exist = False

                # check a column name is exist in final column list
                for index in range(final_column_count):
                    if column_current_item == self.final_column.item(index).text():
                        is_exist = True
                        break

                if is_exist is False:
                    self.final_column.addItem(column_current_item)

            # if list is empty, add item
            else:
                self.final_column.addItem(column_current_item)

    def timeline_list_clicked(self):
        # empty the column list
        self.column_list.clear()

        # add column names to column list
        for column in self.timeline_columns[self.timeline_list.currentItem().text()]:
            self.column_list.addItem(column)

    def remove_column_button_clicked(self):
        column_count = self.final_column.count()
        if column_count > 0:
            self.final_column.takeItem(self.final_column.currentRow())

    def merge_button_clicked(self):
        # select column from each selected timeline
        selected_columns = defaultdict(dict)

        # get timeline name, column type (timestamp or event), and column name
        for index in range(self.final_column.count()):
            text = self.final_column.item(index).text()
            text_split = text.split(': ')
            timeline_name = text_split[0].split('[')[0]
            column_type = text_split[0].split('[')[1].split(']')[0]
            column_name = text_split[1]
            selected_columns[timeline_name][column_type] = column_name

        # insert into (new) table merged timeline
        self.database.insert_into_merged_timeline(selected_columns, self.merged_timeline_table_name)

        # show info dialog: Merge timelines is successful. You can access the file: case_name_merged_timelines.csv
        self.show_info_messagebox("Merge timelines is successful.")

    @staticmethod
    def show_info_messagebox(text):
        dlg = QMessageBox()
        dlg.setWindowTitle("DroneTimeline")
        dlg.setText(text)
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Information)
        dlg.exec_()


def main():
    app = QApplication(sys.argv)
    _ = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
