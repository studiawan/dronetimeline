import MergeTimelineSubWindow

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QListWidget,
    QMessageBox
)

from PyQt5 import QtGui
from collections import defaultdict

@MergeTimelineSubWindow.hookimpl
def show_ui(MergeTimelineSubWindowObj):
    # set title and geometry
    subwindow_title = 'Merge Timelines'
    MergeTimelineSubWindowObj.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
    MergeTimelineSubWindowObj.setWindowTitle(subwindow_title)
    MergeTimelineSubWindowObj.setGeometry(60, 60, 600, 400)

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
    MergeTimelineSubWindowObj.timeline_combo = QComboBox()
    for timeline_name in MergeTimelineSubWindowObj.timeline_columns.keys():
        MergeTimelineSubWindowObj.timeline_combo.addItem(timeline_name)

    # add timeline button
    add_timeline_button = QPushButton(MergeTimelineSubWindowObj)
    add_timeline_button.setText('Add timeline')
    add_timeline_button.clicked.connect(MergeTimelineSubWindowObj.add_timeline_button_clicked)

    # label
    added_timeline_label = QLabel()
    added_timeline_label.setText('Added timeline:')

    # timeline list
    MergeTimelineSubWindowObj.timeline_list = QListWidget()
    MergeTimelineSubWindowObj.timeline_list.itemClicked.connect(MergeTimelineSubWindowObj.timeline_list_clicked)

    # add widget to layout 1
    layout1.addWidget(timeline_label)
    layout1.addWidget(MergeTimelineSubWindowObj.timeline_combo)
    layout1.addWidget(add_timeline_button)
    layout1.addWidget(added_timeline_label)
    layout1.addWidget(MergeTimelineSubWindowObj.timeline_list)

    # add widget to layout 2
    # label
    column_label = QLabel()
    column_label.setText('Columns in selected timeline:')

    # column list
    MergeTimelineSubWindowObj.column_list = QListWidget()

    # add column as timestamp
    add_column_as_timestamp_button = QPushButton()
    add_column_as_timestamp_button.setText('Add column as timestamp')
    add_column_as_timestamp_button.clicked.connect(MergeTimelineSubWindowObj.add_column_as_timestamp_button_clicked)

    # add column as event button
    add_column_as_event_button = QPushButton()
    add_column_as_event_button.setText('Add column as event')
    add_column_as_event_button.clicked.connect(MergeTimelineSubWindowObj.add_column_as_event_button_clicked)

    # add widgets to layout 2
    layout2.addWidget(column_label)
    layout2.addWidget(MergeTimelineSubWindowObj.column_list)
    layout2.addWidget(add_column_as_timestamp_button)
    layout2.addWidget(add_column_as_event_button)

    # add widget to layout 3
    # label
    final_column_label = QLabel()
    final_column_label.setText('Added columns for timeline merging:')

    # added column list
    MergeTimelineSubWindowObj.final_column = QListWidget()

    # remove column button
    remove_column_button = QPushButton()
    remove_column_button.setText('Remove column')
    remove_column_button.clicked.connect(MergeTimelineSubWindowObj.remove_column_button_clicked)

    # merge timeline button
    merge_button = QPushButton()
    merge_button.setText('Merge timeline')
    merge_button.clicked.connect(MergeTimelineSubWindowObj.merge_button_clicked)

    # add widgets to layout 3
    layout3.addWidget(final_column_label)
    layout3.addWidget(MergeTimelineSubWindowObj.final_column)
    layout3.addWidget(remove_column_button)
    layout3.addWidget(merge_button)

    # main layout and main widget
    main_layout.addLayout(layout1)
    main_layout.addLayout(layout2)
    main_layout.addLayout(layout3)
    main_widget.setLayout(main_layout)

    # add subwindow and show
    MergeTimelineSubWindowObj.setWidget(main_widget)
    MergeTimelineSubWindowObj.show()

@MergeTimelineSubWindow.hookimpl
def add_timeline_button_clicked(MergeTimelineSubWindowObj):
    timeline_combo_count = MergeTimelineSubWindowObj.timeline_combo.count()

    # check whether combo is not empty
    if timeline_combo_count > 0:
        timeline_list_count = MergeTimelineSubWindowObj.timeline_list.count()

        # check whether list is not empty
        if timeline_list_count > 0:
            is_exist = False

            # check a timeline name is exist in the list or not
            for index in range(timeline_list_count):
                if MergeTimelineSubWindowObj.timeline_combo.currentText() == MergeTimelineSubWindowObj.timeline_list.item(index).text():
                    is_exist = True
                    break

            # add timeline to list if not exist
            if is_exist is False:
                MergeTimelineSubWindowObj.timeline_list.addItem(MergeTimelineSubWindowObj.timeline_combo.currentText())

        # if list is empty, add item
        else:
            MergeTimelineSubWindowObj.timeline_list.addItem(MergeTimelineSubWindowObj.timeline_combo.currentText())

@MergeTimelineSubWindow.hookimpl
def add_column_as_timestamp_button_clicked(MergeTimelineSubWindowObj):
    MergeTimelineSubWindowObj.add_column_clicked('timestamp')

@MergeTimelineSubWindow.hookimpl
def add_column_as_event_button_clicked(MergeTimelineSubWindowObj):
    MergeTimelineSubWindowObj.add_column_clicked('event')

@MergeTimelineSubWindow.hookimpl
def add_column_clicked(MergeTimelineSubWindowObj, column_type):
    column_count = MergeTimelineSubWindowObj.column_list.count()

    # check whether column list is not empty
    if column_count > 0 and len(MergeTimelineSubWindowObj.column_list.selectedItems()) > 0:
        final_column_count = MergeTimelineSubWindowObj.final_column.count()
        column_current_item = f'{MergeTimelineSubWindowObj.timeline_list.currentItem().text()}{"["}{column_type}{"]: "}' \
                                f'{MergeTimelineSubWindowObj.column_list.currentItem().text()}'

        # check whether final column list is not empty
        if final_column_count > 0:
            is_exist = False

            # check a column name is exist in final column list
            for index in range(final_column_count):
                if column_current_item == MergeTimelineSubWindowObj.final_column.item(index).text():
                    is_exist = True
                    break

            if is_exist is False:
                MergeTimelineSubWindowObj.final_column.addItem(column_current_item)

        # if list is empty, add item
        else:
            MergeTimelineSubWindowObj.final_column.addItem(column_current_item)

@MergeTimelineSubWindow.hookimpl
def timeline_list_clicked(MergeTimelineSubWindowObj):
    # empty the column list
    MergeTimelineSubWindowObj.column_list.clear()

    # add column names to column list
    for column in MergeTimelineSubWindowObj.timeline_columns[MergeTimelineSubWindowObj.timeline_list.currentItem().text()]:
        MergeTimelineSubWindowObj.column_list.addItem(column)

@MergeTimelineSubWindow.hookimpl
def remove_column_button_clicked(MergeTimelineSubWindowObj):
    column_count = MergeTimelineSubWindowObj.final_column.count()
    if column_count > 0:
        MergeTimelineSubWindowObj.final_column.takeItem(MergeTimelineSubWindowObj.final_column.currentRow())

@MergeTimelineSubWindow.hookimpl
def merge_button_clicked(MergeTimelineSubWindowObj):
    column_count = MergeTimelineSubWindowObj.final_column.count()
    if column_count > 0:
        # select column from each selected timeline
        selected_columns = defaultdict(dict)

        # get timeline name, column type (timestamp or event), and column name
        for index in range(MergeTimelineSubWindowObj.final_column.count()):
            text = MergeTimelineSubWindowObj.final_column.item(index).text()
            text_split = text.split(': ')
            timeline_name = text_split[0].split('[')[0]
            column_type = text_split[0].split('[')[1].split(']')[0]
            column_name = text_split[1]
            selected_columns[timeline_name][column_type] = column_name

        # insert into (new) table merged timeline
        MergeTimelineSubWindowObj.database.insert_into_merged_timeline(selected_columns, MergeTimelineSubWindowObj.merged_timeline_table_name)

        # show info dialog: Merge timelines is successful. You can access the file: case_name_merged_timelines.csv
        MergeTimelineSubWindowObj.show_info_messagebox("Merge timelines is successful.")

@MergeTimelineSubWindow.hookimpl
def show_info_messagebox(text):
    dlg = QMessageBox()
    dlg.setWindowTitle("DroneTimeline")
    dlg.setText(text)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.setIcon(QMessageBox.Information)
    dlg.exec_()
