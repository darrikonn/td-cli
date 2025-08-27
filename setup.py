from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="td-cli",
    version="2.2.2",
    description="A todo command line manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darrikonn/td-cli",
    author="Darri Steinn Konn Konradsson",
    author_email="darrikonn@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="todo commandline td-cli",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.6",
    install_requires=[],
    entry_points={"console_scripts": ["td=todo:main"]},
    project_urls={"Source": "https://github.com/darrikonn/td-cli"},
)
