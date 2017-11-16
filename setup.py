import ast
import re

from setuptools import setup, find_packages

from io import open

# get __version__ from __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jsoncore/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# load README.rst
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name="jsoncore",
    version=version,
    url="https://github.com/json-transformations/jsoncore",
    keywords=[],

    author="Brian Peterson",
    author_email="bpeterso2000@yahoo.com",

    description="Package description.",
    long_description=readme,

    packages=find_packages(include=['jsoncore']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'click==6.7',
        'contextlib2==0.5.5',
        'jsoncrawl==1.1',
        'toolz'
    ],
    test_suite='tests',
    test_requires=[
        'pytest-cov==2.5.1',
        'flake8==3.5.0',
        'tox==2.9.1'
    ],
    setup_requires=['pytest-runner'],
)
