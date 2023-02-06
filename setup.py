from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

setup(
    name="bayesian_classifier",
    version="1.0.0",
    description='Python library for training and testing Bayesian classifiers',
    classifiers=[],
    keywords=['bayesian', 'classifier'],
    url='https://github.com/mathbarc/bayesian-classifier',
    packages=find_packages(exclude=["tests", "experiments", "docs"]),
    include_package_data=True,
    license="MIT",
    zip_safe=True,
    install_requires=[
        'click>=8.1.3',
        'numpy>=1.23.5'
    ],
    entry_points='''
        [console_scripts]
            bayesian_classifier = bayesian_classifier.__main__:cli
            ''',
)
