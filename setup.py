from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='todo',
    version='0.0.1',
    description='A todo command line tool',
    url='https://github.com/darrikonn/todo',
    author='Darri Steinn Konn Konradsson',
    author_email='darrikonn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Command line enthusiasts',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='todo commandline',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'todo=todo:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/darrikonn/todo',
    },
)
