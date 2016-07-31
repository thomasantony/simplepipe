import os
from setuptools import setup
import simplepipe
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "simplepipe",
    version = simplepipe.__version__,
    author = "Thomas Antony",
    author_email = "tantony.purdue@gmail.com",
    description = ("A simple functional pipelining library for Python."),
    license = "MIT",
    keywords = "pipeline, functional, functional programming",
    url = "https://github.com/thomasantony/simplepipe",
    py_modules=['simplepipe'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
    ],
)
