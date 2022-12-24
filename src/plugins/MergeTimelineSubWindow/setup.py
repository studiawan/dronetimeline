from setuptools import setup, find_packages

setup(
    name="MergeTimelineSubWindow",
    version="1.0.0",
    description="MergeTimelineSubWindow",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["MergeTimelineSubWindow = MergeTimelineSubWindow.host:main"]
    },
    install_requires=[
        "pluggy",
        "PyQt5"
    ]
)