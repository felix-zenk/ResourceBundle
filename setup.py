import re

import setuptools
import toml

from pathlib import Path

pyproject = toml.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
author = pyproject['project']['authors'][0]

setuptools.setup(
    name=pyproject['project']['name'],
    description=pyproject['project']['description'],
    version=pyproject['project']['version'],
    author=author['name'],
    author_email=author['email'],
    license=pyproject['project']['license'],
    long_description=Path(pyproject['project']['readme']['file']).read_text(encoding='utf-8'),
    long_description_content_type=pyproject['project']['readme']['content-type'],
    url=pyproject['project']['urls']['Homepage'],
    project_urls={k: v for k, v in pyproject['project']['urls'].items() if k != 'Homepage'},
    packages=setuptools.find_packages(
        where=pyproject['tool']['setuptools']['packages']['find'].get('where', '.'),
        include=pyproject['tool']['setuptools']['packages']['find']['include']
    ),
    requires=[
        re.match(r'([\w-]+)', dependency).group(1)
        for dependency in pyproject['project']['dependencies']
    ],
    classifiers=pyproject['project']['classifiers'],
    keywords=pyproject['project']['keywords'],
    python_requires=pyproject['project']['requires-python'],
)
