from setuptools import find_packages, setup
from typing import List

requirement_file_name = "requirements.txt"
REMOVE_PACKAGE = "-e ."

def get_requirements_file() -> List[str]:
    with open(requirement_file_name) as requirement_file:
        requirements_list = requirement_file.readline()
    requirements_list = [requirement_name.replace("\n","") for requirement_name in requirements_list]

    if REMOVE_PACKAGE in requirements_list:
        requirements_list.remove(REMOVE_PACKAGE)

    return requirements_list

setup(
    name='ippredictor',
    version="0.0.1",
    description="Insurance Premium Prediction",
    author="Pradeep.P",
    author_email="pradeep.pvj8@gmail.com",
    url="https://github.com/pradeeppvj8/Insurance-Premium-Prediction",
    packages=find_packages(),
    install_reqires = get_requirements_file()
)