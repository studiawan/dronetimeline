import pluggy

hookspec = pluggy.HookspecMarker("MergeTimelineSubWindow")
"""Marker to be imported and used in plugins (and for own implementations)"""

@hookspec(firstresult=True)
def show_ui(MergeTimelineSubWindowObj):
    """Show the merge timeline config sub window

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def add_timeline_button_clicked(MergeTimelineSubWindowObj):
    """Add timeline button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def add_column_as_timestamp_button_clicked(MergeTimelineSubWindowObj):
    """Add column as timestamp button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def add_column_as_event_button_clicked(MergeTimelineSubWindowObj):
    """Add column as event button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def add_column_clicked(MergeTimelineSubWindowObj, column_type):
    """Add column button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :param column_type: type of the column
    :return: None
    """

@hookspec(firstresult=True)
def timeline_list_clicked(MergeTimelineSubWindowObj):
    """Timeline list clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def remove_column_button_clicked(MergeTimelineSubWindowObj):
    """Remove column button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def merge_button_clicked(MergeTimelineSubWindowObj):
    """Merge button clicked

    :param MergeTimelineSubWindowObj: MergeTimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def show_info_messagebox(text):
    """Show an info message box

    :param text: text to be shown
    :return: None
    """