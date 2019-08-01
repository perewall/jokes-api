import io
import re
import os
import sys


sys.path.insert(0, os.path.abspath('../'))


with io.open('../jokes_api/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


project = 'Jokes API'
copyright = '2019'
language = 'en'
html_theme = 'sphinx_rtd_theme'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinxcontrib.autohttp.flask',
    'sphinxcontrib.autohttp.flaskqref']
