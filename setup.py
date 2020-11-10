import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phypster",
    version="0.0.1-Beta",
    author="Vincent DONVAL",
    author_email="vincent1donval@gmail.com",
    description="Jhypster for python developper. Flask starter \n\n #Jhypster #Python #Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincauddu29/phypster",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'Jinja2==2.10.1',
          'inquirer==2.7.0',
    ],
    entry_points={
        'console_scripts': [
            'phypster=phypster:main'
        ]
    }
)