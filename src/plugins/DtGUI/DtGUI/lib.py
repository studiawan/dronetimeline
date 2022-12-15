import DtGUI, os, re
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
from QtDatabase import host as QtDatabase_Plugin
from TimelineSubWindow import host as TimelineSubWindow_Plugin
from MergeTimelineSubWindow import host as MergeTimelineSubWindow_Plugin

@DtGUI.hookimpl
def init_ui(DtGUIObj):
    DtGUIObj.statusBar()
    # show main window
    DtGUIObj.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
    DtGUIObj.setGeometry(50, 50, 800, 600)
    DtGUIObj.setWindowTitle(DtGUIObj.main_window_title)
    DtGUIObj.show()

@DtGUI.hookimpl
def init_menu(DtGUIObj):
    # application menu
    menubar = DtGUIObj.menuBar()

    # File menu
    file_menu = menubar.addMenu('&File')
    file_menu.addAction(DtGUIObj.newcase_action())
    file_menu.addAction(DtGUIObj.import_action())
    file_menu.addAction(DtGUIObj.exit_action())

    # Timeline menu
    timeline_menu = menubar.addMenu('&Timeline')
    timeline_menu.addAction(DtGUIObj.merge_action())
    timeline_menu.addAction(DtGUIObj.show_merged_timeline_action())

@DtGUI.hookimpl
def newcase_action(DtGUIObj):
    newcase_act = QAction('&Select Case Directory', DtGUIObj)
    newcase_act.setShortcut('Ctrl+N')
    newcase_act.setStatusTip('Select case directory')
    newcase_act.triggered.connect(DtGUIObj.open_directory_dialog)

    return newcase_act

@DtGUI.hookimpl
def import_action(DtGUIObj):
    import_act = QAction('&Import Timeline', DtGUIObj)
    import_act.setShortcut('Ctrl+I')
    import_act.setStatusTip('Import timeline')
    import_act.triggered.connect(DtGUIObj.open_file_dialog)

    return import_act

@DtGUI.hookimpl
def exit_action(DtGUIObj):
    exit_act = QAction('&Exit', DtGUIObj)
    exit_act.setShortcut('Ctrl+Q')
    exit_act.setStatusTip('Exit application')
    exit_act.triggered.connect(qApp.quit)

    if DtGUIObj.database is not None:
        DtGUIObj.database.connection.close()

    return exit_act

@DtGUI.hookimpl
def merge_action(DtGUIObj):
    merge_act = QAction('&Merge Timelines', DtGUIObj)
    merge_act.setShortcut('Ctrl+M')
    merge_act.setStatusTip('Merge timelines')
    merge_act.triggered.connect(DtGUIObj.merge_window_trigger)

    return merge_act

@DtGUI.hookimpl
def show_merged_timeline_action(DtGUIObj):
    show_merged_timeline_act = QAction('S&how Merged Timeline', DtGUIObj)
    show_merged_timeline_act.setShortcut('Ctrl+H')
    show_merged_timeline_act.setStatusTip('Show merged timeline')
    show_merged_timeline_act.triggered.connect(DtGUIObj.merged_timeline_window_trigger)

    return show_merged_timeline_act

@DtGUI.hookimpl
def open_directory_dialog(DtGUIObj):
    directory = QFileDialog.getExistingDirectory(DtGUIObj, "Select Directory")

    # get database name and database directory
    database_name = os.path.basename(directory)
    if database_name != '' and directory != '':
        DtGUIObj.database = QtDatabase_Plugin.QtDatabase(directory)

        # case name == database name
        DtGUIObj.case_name = database_name
        DtGUIObj.case_directory = directory

        message = f'{"Case directory is selected: "}{directory}'
        DtGUIObj.show_info_messagebox(message)

@DtGUI.hookimpl
def open_file_dialog(DtGUIObj):
    if DtGUIObj.case_name == '':
        DtGUIObj.show_info_messagebox("Please select case directory before importing a timeline.")

    else:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(DtGUIObj, "Open file", "", "All Files (*)",
                                                    options=options)
        if file_name:
            print(file_name)

            # insert timeline to database
            table_name = os.path.basename(file_name)
            table_name = os.path.splitext(table_name)[0]

            # make sure table name is alphanumeric
            table_name = re.sub('[\W_]+', '', table_name)

            # insert csv file to database
            column_names = DtGUIObj.database.insert_csv(table_name, file_name)
            print("COLUMN NAMES", column_names)

            # save timeline and its column names
            DtGUIObj.timeline_columns[table_name] = column_names

            # show timeline in an MDI window
            DtGUIObj.timeline_subwindow_trigger(table_name, column_names)
            message = f'{"Timeline is imported successfully: "}{table_name}{"."}'
            DtGUIObj.show_info_messagebox(message)

@DtGUI.hookimpl
def timeline_subwindow_trigger(DtGUIObj, table_name, column_names):
    # define and show timeline sub window
    subwindow = TimelineSubWindow_Plugin.TimelineSubWindow(table_name, column_names, DtGUIObj.database.connection)
    DtGUIObj.mdi.addSubWindow(subwindow)
    subwindow.show_ui()

@DtGUI.hookimpl
def merge_window_trigger(DtGUIObj):
    # define and show merge timeline config sub window
    subwindow = MergeTimelineSubWindow_Plugin.MergeTimelineSubWindow(DtGUIObj.timeline_columns, DtGUIObj.database, DtGUIObj.merged_timeline_table_name)
    DtGUIObj.mdi.addSubWindow(subwindow)
    subwindow.show_ui()

@DtGUI.hookimpl
def merged_timeline_window_trigger(DtGUIObj):
    if DtGUIObj.database is None:
        DtGUIObj.show_info_messagebox('Please select case directory, import timeline, and then merge timeline.')

    else:
        # define and show merged timeline sub window
        subwindow = TimelineSubWindow_Plugin.TimelineSubWindow(DtGUIObj.merged_timeline_table_name,
                                        ['timestamp', 'event'], DtGUIObj.database.connection)
        DtGUIObj.mdi.addSubWindow(subwindow)
        subwindow.show_ui()

@DtGUI.hookimpl
def show_info_messagebox(text):
    dlg = QMessageBox()
    dlg.setWindowTitle("DroneTimeline")
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Information)
    dlg.exec_()