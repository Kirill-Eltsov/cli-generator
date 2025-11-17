from setuptools import setup, find_packages

setup(
    name="data-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click>=8.0.0", "Faker>=15.0.0"],
    entry_points={'console_scripts': ['datagen=cli.commands:cli']},
)
