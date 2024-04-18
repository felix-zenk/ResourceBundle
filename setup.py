import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


with open('pyproject.toml', mode='r', encoding='utf-8') as f:
    version = f.read().split('version = ')[1].split('\n')[0].strip().replace('"', '')


setuptools.setup(
    name="ResourceBundle",
    version=version,
    author='Felix Zenk',
    author_email='felix.zenk@web.de',
    description="ResourceBundle is a module that manages internationalization of string resources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felix-zenk/ResourceBundle",
    project_urls={
        "Issues": "https://github.com/felix-zenk/ResourceBundle/issues",
        "Repository": "https://github.com/felix-zenk/ResourceBundle",
        "Documentation": "https://github.com/felix-zenk/ResourceBundle",
    },
    packages=setuptools.find_packages(".", include=["ResourceBundle*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Utilities',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5'
)
