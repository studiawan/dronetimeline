from setuptools import setup

setup(
    name="DtGUI-plugin-example",
    version="1.0.0",
    description="DtGUI-plugin-example",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    entry_points={
        "DtGUI": ["plugin-example = add_new_menu"],
    },
    install_requires=[
        "DtGUI",
    ]
)