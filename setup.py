import setuptools

import src.phypster

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phypster",
    version="0.0.1",
    packages=setuptools.find_packages('phypster'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'Jinja2==2.10.1',
          'inquirer==2.7.0',
    ]
)