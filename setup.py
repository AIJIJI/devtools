#!/bin/python3
from setuptools import setup

setup(
    name='AIJIdevtools',
    version='1.1',
    author='AIJI',
    author_email='thecrazyaiji@gmail.com',
    description='Some useful helper-funcs for devpers',
    packages=['devtools'],
    install_requires=[
        'sh',
        'sqlparse',
        'termcolor'
    ],
    url='https://github.com/AIJIJI/devtools',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Framework :: Flask",
        "Development Status :: 1 - Planning"
    ]
)
