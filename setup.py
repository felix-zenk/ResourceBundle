import setuptools
from ResourceBundle import __version__, __author__, __email__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

homepage = "https://felix-zenk.github.io/projects/ResourceBundle"
source = "https://github.com/felix-zenk/ResourceBundle"


setuptools.setup(
    name="ResourceBundle",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="ResourceBundle is a module that manages internationalization of string resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=homepage,
    project_urls={
        "Bug Reports": f"{source}/issues",
        "Source": source
    },
    packages=setuptools.find_packages(".", exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
