import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JST_analysis",
    version="0.0.3",
    author="Mikołaj Boroński",
    author_email="m.boronski@student.uw.edu.pl",
    description="JST analysis package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Laz4rz/NYPD_Project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas==1.4.0",
        "numpy==1.22.2",
        "tqdm~=4.62.3",
        "openpyxl==3.0.9",
        "xlrd==2.0.1",
    ],
)
