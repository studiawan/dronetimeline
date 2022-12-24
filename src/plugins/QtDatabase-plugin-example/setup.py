from setuptools import setup

setup(
    name="QtDatabase-plugin-example",
    version="1.0.0",
    description="QtDatabase-plugin-example",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    entry_points={
        "QtDatabase": ["plugin-example = qtdatabase_edit_csv"],
    },
    install_requires=[
        "QtDatabase",
    ]
)