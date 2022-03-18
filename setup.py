import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unitexpr",
    version="0.1.6",
    author="D Reschner",
    author_email="git@simphotonics.com",
    description="Units, unit expressions, and united arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simphotonics/unitexpr",
    project_urls={
        "Bug Tracker": "https://github.com/simphotonics/unitexpr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "lockattrs",
    ],
)
