from setuptools import setup
from dbjson import __version__

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="dbjsonpy",
    version=__version__,
    author="Jak Bin",
    author_email="jakbin4747@gmail.com",
    description="crud operation with database using json.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/jakbin/dbjson",
    python_requires=">=3",
    install_requires=["sqlalchemy"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords='dbjson, database, json',
    packages=["dbjson"],
    zip_safe=False,
)
