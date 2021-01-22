import setuptools

# Get Readme from root directory (which will be used for package long_description)
with open("README.md", "r") as fh:
    long_description = fh.read()

# Get any requirements for installation from requirements.txt
with open("requirements.txt", "r") as fh:
    requires = fh.read().splitlines()

setuptools.setup(
    name="regridMerra",
    description="Regrids MERRA to AIRS L3 grid",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=["regrid.py", "plot.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requires,
)
