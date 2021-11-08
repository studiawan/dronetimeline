import sys
import os
import re
import time
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea
)
from PyQt5 import QtGui
from qtdatabase import QtDatabase
from timeline_subwindow import TimelineSubWindow
from merge_timeline_subwindow import MergeTimelineSubWindow


class DtGui(QMainWindow):

    ansel_signal_receiver = pyqtSignal(str, list)

    def __init__(self):
        super().__init__()
        self.main_window_title = 'DroneTimeline: Forensic Timeline Analysis for Drones'
        self.database = None
        self.case_name = ''
        self.case_directory = ''
        self.timeline_columns = {}
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.merged_timeline_table_name = 'mergedtimeline'
        self.init_ui()

        self.ansel_signal_receiver.connect(self.timeline_subwindow_trigger)

    def asdf(self, ass, df):
        print(ass, df)

    def init_ui(self):
        self.statusBar()

        # application menu
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(self.newcase_action())
        file_menu.addAction(self.import_action())
        file_menu.addAction(self.exit_action())

        # Timeline menu
        timeline_menu = menubar.addMenu('&Timeline')
        timeline_menu.addAction(self.merge_action())
        timeline_menu.addAction(self.show_merged_timeline_action())

        # show main window
        self.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle(self.main_window_title)
        self.show()

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

    def merge_action(self):
        merge_act = QAction('&Merge Timelines', self)
        merge_act.setShortcut('Ctrl+M')
        merge_act.setStatusTip('Merge timelines')
        merge_act.triggered.connect(self.merge_window_trigger)

        return merge_act

    def show_merged_timeline_action(self):
        show_merged_timeline_act = QAction('S&how Merged Timeline', self)
        show_merged_timeline_act.setShortcut('Ctrl+H')
        show_merged_timeline_act.setStatusTip('Show merged timeline')
        show_merged_timeline_act.triggered.connect(self.merged_timeline_window_trigger)

        return show_merged_timeline_act

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        # get database name and database directory
        database_name = os.path.basename(directory)
        if database_name != '' and directory != '':
            self.database = QtDatabase(directory)

            # case name == database name
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
                column_names = self.database.insert_csv(self, table_name, file_name)

                # save timeline and its column names
                self.timeline_columns[table_name] = column_names
                
                
                # self.timeline_subwindow_trigger(table_name, column_names)
                

    def timeline_subwindow_trigger(self, table_name, column_names):

        # define timeline sub window
        subwindow = TimelineSubWindow(table_name, column_names, self.database.connection)
        
        # show timeline in an MDI window
        self.mdi.addSubWindow(subwindow)
        subwindow.show_ui()

        # Notification
        message = f'{"Timeline is imported successfully: "}{table_name}{"."}'
        self.show_info_messagebox(message)


    def merge_window_trigger(self):
        # define and show merge timeline config sub window
        subwindow = MergeTimelineSubWindow(self.timeline_columns, self.database, self.merged_timeline_table_name)
        self.mdi.addSubWindow(subwindow)
        subwindow.show_ui()

    def merged_timeline_window_trigger(self):
        if self.database is None:
            self.show_info_messagebox('Please select case directory, import timeline, and then merge timeline.')

        else:
            # define and show merged timeline sub window
            subwindow = TimelineSubWindow(self.merged_timeline_table_name,
                                          ['timestamp', 'event'], self.database.connection)
            self.mdi.addSubWindow(subwindow)
            subwindow.show_ui()

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
    _ = DtGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
