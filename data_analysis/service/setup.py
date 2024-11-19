from setuptools import setup, find_packages

setup(
    name='time_series_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels'
    ],
)
