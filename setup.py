#!/bin/python3
from setuptools import setup

setup(
    name='AIJIdevtools',
    version='0.3.4',
    author='AIJI',
    author_email='thecrazyaiji@gmail.com',
    description='Some useful helper-funcs for devpers',
    packages=['devtools'],
    install_requires=['psutil', 'sqlparse', 'termcolor'],
    url='https://github.com/AIJIJI/devtools'
)
