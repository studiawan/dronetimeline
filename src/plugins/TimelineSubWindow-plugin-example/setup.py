from setuptools import setup

setup(
    name="TimelineSubWindow-plugin-example",
    version="1.0.0",
    description="TimelineSubWindow-plugin-example",
    author="Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    url="",
    entry_points={
        "TimelineSubWindow": ["plugin-example = plugin"],
    },
    install_requires=[
        "TimelineSubWindow",
    ]
)