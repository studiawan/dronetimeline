from setuptools import setup, find_packages

setup(
    name="dronetimeline",
    version="1.0.0",
    description="DroneTimeline",
    author="Hudan Studiawan",
    author_email="hudan@its.ac.id",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["dronetimeline = src.dtgui:main "]
    },
    install_requires=[
        "pluggy",
        "PyQt5",
        "spacy",
        "DtGUI",
        "MergeTimelineSubWindow",
        "QtDatabase",
        "TimelineSubWindow"
    ]
)