
"""
pycricket
"""

__title__ = 'pycricket'
__version__ = '0.1'
__author__ = 'Shivam Mitra'
__license__ = 'GPLv2'


import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, path)

