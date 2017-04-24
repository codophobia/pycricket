from setuptools import setup,find_packages
setup(
  name = 'pycricket',
  packages=['pycricket'],  # include all packages under src
  version = '1.0',
  description = 'A library for fetching cricket scorecards of past cricket matches',
  author = 'Shivam Mitra',
  author_email = 'shivamm389@gmail.com',
  license = 'GPLv2',
  url = 'https://github.com/codophobia/cricket-scorecards-and-commentary-with-python', 
  download_url = 'https://github.com/codophobia/cricket-scorecards-and-commentary-with-python/tarball/0.2', 
  keywords = ['cricket', 'scorecards'], 
  install_requires=[
          'beautifulsoup4'
      ],
  classifiers = [],

  package_data={'pycricket': ['matches.csv']},
  
  include_package_data=True,
)

