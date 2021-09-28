import setuptools
import re
from ResourceBundle import __version__, __author__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

    # Don't display badge on PyPI
    long_description = re.sub(r"\[!\[PyPI version.*\d+\.\d+\.\d+.*yellow\)\]\(.*project/ResourceBundle\)", "",
                              long_description)

url = "https://github.com/felix-zenk/ResourceBundle"

setuptools.setup(
    name="ResourceBundle",
    version=__version__,
    author=__author__.split("<")[0].strip(),
    author_email=re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})", __author__).group(1),
    description="ResourceBundle is a module that manages resource handling where different resources are needed " +
                "depending on the current locale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls={
        "Bug Reports": url+"/issues/new?labels=bug&template=bug_report.md&title=%5BBUG%5D%3A+",
        "Source": url
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
