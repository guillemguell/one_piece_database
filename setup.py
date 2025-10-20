from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
  '''
  This function returns the list of requirements
  '''
  requirements = []
  with open(file_path) as f:
    requirements = f.readlines()
    requirements = [req.replace('\n','') for req in requirements]

    if HYPHEN_E_DOT in requirements:
      requirements.remove(HYPHEN_E_DOT)

  return requirements

setup(
    name = 'One Piece database',
    version = '1.0.0',
    description = "One Piece entities Database",
    author = 'Guillem Güell',
    packages = find_packages(),
    python_requires = '>=3.0',
    install_requires = get_requirements('requirements.txt'),
    # extras_require = {
    #     'dev': ['pdoc',
    #             'pylint',
    #             'coverage'],
    # },
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ],
)
