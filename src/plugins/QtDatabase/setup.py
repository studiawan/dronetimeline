from setuptools import setup, find_packages

setup(
    name="QtDatabase",
    version="1.0.0",
    description="QtDatabase",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["QtDatabase = QtDatabase.host:main"]
    },
    install_requires=[
        "pluggy",
        "PyQt5"
    ]
)