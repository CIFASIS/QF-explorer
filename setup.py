#!/usr/bin/python2
from setuptools import setup

setup(
    name='QF-explorer',
    version='0.1',
    packages=['src'],
    #include_package_data=True,
    license='GPL3',
    description='???',
    long_description="",
    url='http://QuickFuzz.org/',
    author='G.Grieco',
    author_email='gg@cifasis-conicet.gov.ar',
    scripts=[
        'qf-exp.py'
        ],
    install_requires=[
        "cma"
        ],
)
