from setuptools import setup, find_packages

setup(
    name='finance',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'yfinance'
    ],
)
