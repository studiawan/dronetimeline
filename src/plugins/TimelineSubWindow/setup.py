from setuptools import setup, find_packages

setup(
    name="TimelineSubWindow",
    version="1.0.0",
    description="TimelineSubWindow",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["TimelineSubWindow = TimelineSubWindow.host:main"]
    },
    install_requires=[
        "pluggy",
        "PyQt5"
    ]
)