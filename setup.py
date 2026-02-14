from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cadmies-demo",
    version="1.1.0",
    author="Project Hieros - CADMIES-IPLD Research Group",
    author_email="hieroscadmies@proton.me",
    description="CADMIES Demo - Test the IPLD Knowledge System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hieros-CADMIES/CADMIES",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
)
