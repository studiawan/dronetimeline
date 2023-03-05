# DroneTimeline
DroneTimeline is a forensic timeline analysis tool for drone.

## Requirements

- Python 3.8
- PyQt5
- pluggy 1.0.0

## How to run

- Clone the repository
  ```bash
  git clone https://github.com/studiawan/dronetimeline.git
  ```
- Setup virtual environment
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment
  ```bash
  source venv/bin/activate
  ```
- Install the requirements
  ```bash
  pip install -r requirements.txt
  ```
- Run setup.py
  ```bash
  python setup.py install
  ```
- Run the DroneTimeLine application
  ```bash
  dronetimeline
  ```

- The order of the run: select case directory, import timeline, merge the timelines, and show merged timeline.
- To select case directory, choose *File* &#8594; *Select Case Directory*
- To import timeline, click *File* &#8594; *Import Timeline*
- We then can merge the imported timelines by clicking *Timeline* &#8594; *Merge Timelines*
- Finally, we can check the merged timeline by choosing *Timeline* &#8594; *Show Merged Timeline*

## How to create and install your own plugin

For example, we want to create a plugin to add a new menu to the menu bar. The plugin name is `DtGUI-myplugin` and the plugin is implementing `DtGUI` hookspecs.

- Create a new directory `DtGUI-myplugin` in `src/plugins`.
- Create a new file for example `add_new_menu.py` in the `DtGUI-myplugin` directory. This file will contain the implementation of the [DtGUI hookspecs](src/plugins/DtGUI/DtGUI/hookspecs.py). For example we want to add a new menu into menu bar, we can implement the `init_menu` hookspecs. The implementation is as follows:
  ```python
  import DtGUI
  from PyQt5.QtWidgets import (
      QAction,
  )

  @DtGUI.hookimpl
  def init_menu(DtGUIObj):
      # application menu
      menubar = DtGUIObj.menuBar()

      # File menu
      new_menu = menubar.addMenu('&New Customized Menu')
      
      # File menu action
      newmenu_act = QAction('&Select something', DtGUIObj)
      newmenu_act.setShortcut('Ctrl+P')
      newmenu_act.setStatusTip('Select something')

      def newmenu_trigger():
          DtGUIObj.show_info_messagebox('You have selected the new menu')

      newmenu_act.triggered.connect(newmenu_trigger)
      new_menu.addAction(newmenu_act)
  ```
- Create a new file `setup.py` in the `DtGUI-myplugin` directory to package and distribute the plugin. The content of the `setup.py` is as follows:
  ```python
  from setuptools import setup

  setup(
      name="DtGUI-myplugin",
      version="1.0.0",
      description="DtGUI-myplugin",
      author="Your Name",
      author_email="example@example.com",
      url="",
      entry_points={
          "DtGUI": ["myplugin = add_new_menu"],
      },
      install_requires=[
          "DtGUI",
      ]
  )
  ```
- Install the plugin
  ```bash
  pip install --editable src/plugins/DtGUI-myplugin
  ```

## License
MIT License.