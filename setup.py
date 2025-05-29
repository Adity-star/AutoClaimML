# setup.py
from setuptools import setup, find_packages
import setuptools
from pathlib import Path


__version__ = "0.1.0"

REPO_NAME = "AutoClaimML"
AUTHOR_USER_NAME = "Aditya AK"
SRC_REPO = "VehicleInsurance"
AUTHOR_EMAIL = "aakuskar.980@gmail.com"

setup(
    name=SRC_REPO, 
    version=__version__,  # Incremented version for initial release
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="An MLOps pipeline for vehicle insurance risk prediction",
    long_description=open("README.md").read() if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",  
    project_urls={
        "Bug Tracker":  f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(where="src"), 
    package_dir={"": "src"},  # Tell setuptools where to find the packages
)   
