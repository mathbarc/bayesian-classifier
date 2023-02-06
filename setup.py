from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
README = (this_directory/ "README.md").read_text()

setup(
    name="bayesian_classifier",
    version="1.0.0",
    description='Python library for training and testing Bayesian classifiers',
    long_description_content_type="text/markdown",
    long_description=README,
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
