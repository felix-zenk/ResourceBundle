import setuptools
import re
from ResourceBundle import __version__, __author__, __email__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

    # Don't display badge on PyPI
    long_description = re.sub(r"\[!\[PyPI version.*\d+\.\d+\.\d+.*yellow\)\]\(.*project/ResourceBundle\)", "",
                              long_description)

homepage = "https://felix-zenk.github.io/projects/ResourceBundle"
source = "https://github.com/felix-zenk/ResourceBundle"


setuptools.setup(
    name="ResourceBundle",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="ResourceBundle is a module that manages resource handling where different resources are needed " +
                "depending on the current locale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=homepage,
    project_urls={
        "Bug Reports": source+"/issues/new?labels=bug&template=bug_report.md&title=%5BBUG%5D%3A+",
        "Source": source
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
