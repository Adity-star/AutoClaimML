# setup.py
from setuptools import setup, find_packages
import setuptools
from pathlib import Path


__version__ = "0.1.0"
PACKAGE_NAME = "AutoClaimML"  
GITHUB_USERNAME = "aakuskar" 
AUTHOR_NAME = "Aditya AK"
AUTHOR_EMAIL = "aakuskar.980@gmail.com"

# Read long description from README.md if exists
long_description = ""
readme_path = Path("README.md")
if readme_path.exists():
    long_description = readme_path.read_text()

setup(
    name=PACKAGE_NAME,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="An MLOps pipeline for vehicle insurance risk prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{GITHUB_USERNAME}/{PACKAGE_NAME}",
    packages=find_packages(where="src"),
    package_dir={"": "src"}, 
)   
