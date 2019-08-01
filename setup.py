import io
import re

from setuptools import setup


with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()


with io.open('jokes_api/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='Jokes-API',
    version=version,
    url='https://github.com/perewall/jokes-api',
    license='MIT',
    description='Jokes management API',
    long_description=readme,
    long_description_content_type='text/x-rst',
    python_requires='>= 3.6',
    platforms=['any'],
    install_requires=[
        'flask >= 1.1.1',
        'flask_sqlalchemy >= 2.4.0',
        'flask_migrate >= 2.5.2',
        'flask_login >= 0.4.1',
        'requests >= 2.22.0',
        'python_dotenv >= 0.10.3'
    ],
    tests_require=['responses >= 0.10'],
    entry_points={'console_scripts': ['jokes-api = jokes_api.cli:cli']},
    packages=['jokes_api'],
    package_data={'jokes_api': ['migrations/*', 'migrations/versions/*']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]
)
