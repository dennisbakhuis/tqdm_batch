import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tqdm_batch",
    version="0.1.0",
    author="Dennis Bakhuis",
    author_email="pypi@bakhuis.nu",
    description="Wrapper for tqdm and joblib to have a progressbar while batch processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dennisbakhuis/tqdm_batch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
