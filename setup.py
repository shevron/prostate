from os import path
from setuptools import find_packages, setup

import prostate as p

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='prostate',
    url='https://github.com/shevron/prostate',
    description='Prostate - Testing-oriented Graphical HTTP Client',
    author='Shahar Evron',
    author_email='shahar.evron@gmail.com',
    install_requires=[
        'pygobject',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        prostate=prostate.main:main
    ''',
    packages=find_packages('prostate'),
    version=p.__version__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={'prostate': ['ui/*']},
    include_package_data=True,
)
