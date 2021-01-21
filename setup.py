import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comdirect-api-simple",
    version="0.0.10",
    author="Alexander Knittel",
    author_email="alx.kntl@gmail.com",
    description="A package for read operations for the comdirect API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-kn/comdirect-api-simple",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
