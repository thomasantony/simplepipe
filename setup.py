import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "simplepipe",
    version = "0.0.1",
    author = "Thomas Antony",
    author_email = "tantony.purdue@gmail.com",
    description = ("A simple functional pipelining library for Python."),
    license = "MIT",
    keywords = "pipline, functional, functional programming",
    url = "http://pypi.python.org/pypi/simplepipe",
    packages=['simplepipe', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
