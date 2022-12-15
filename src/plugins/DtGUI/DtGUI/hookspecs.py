import pluggy

hookspec = pluggy.HookspecMarker("DtGUI")
"""Marker to be imported and used in plugins (and for own implementations)"""

@hookspec(firstresult=True)
def init_ui(DtGUIObj):
    """Initialize the user interface

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec
def init_menu(DtGUIObj):
    """Initialize the menu

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec(firstresult=True)
def newcase_action(DtGUIObj):
    """Create a new case action

    :param DtGUIObj: DtGUI object
    :return: QAction object
    """

@hookspec(firstresult=True)
def import_action(DtGUIObj):
    """Create an import action

    :param DtGUIObj: DtGUI object
    :return: QAction object
    """

@hookspec(firstresult=True)
def exit_action(DtGUIObj):
    """Create an exit action

    :param DtGUIObj: DtGUI object
    :return: QAction object
    """

@hookspec(firstresult=True)
def merge_action(DtGUIObj):
    """Create a merge action

    :param DtGUIObj: DtGUI object
    :return: QAction object
    """

@hookspec(firstresult=True)
def show_merged_timeline_action(DtGUIObj):
    """Create a show merged timeline action

    :param DtGUIObj: DtGUI object
    :return: QAction object
    """

@hookspec(firstresult=True)
def open_directory_dialog(DtGUIObj):
    """Open a directory dialog

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec(firstresult=True)
def open_file_dialog(DtGUIObj):
    """Open a file dialog

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec(firstresult=True)
def timeline_subwindow_trigger(DtGUIObj, table_name, column_names):
    """Create a timeline subwindow

    :param DtGUIObj: DtGUI object
    :param table_name: name of the table
    :param column_names: list of column names
    :return: None
    """

@hookspec(firstresult=True)
def merge_window_trigger(DtGUIObj):
    """Create a merge window

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec(firstresult=True)
def merged_timeline_window_trigger(DtGUIObj):
    """Create a merged timeline window

    :param DtGUIObj: DtGUI object
    :return: None
    """

@hookspec(firstresult=True)
def show_info_messagebox(text):
    """Show an info message box

    :param text: message to be shown
    :return: None
    """