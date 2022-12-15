from setuptools import setup, find_packages

setup(
    name="DtGUI",
    version="1.0.0",
    description="DtGUI",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["DtGUI = DtGUI.host:main"]
    },
    install_requires=[
        "pluggy",
        "PyQt5"
    ]
)