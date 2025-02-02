from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cira",
    version="4.0.0",
    description="A simpler library for the alapaca trade api",
    url="https://github.com/AxelGard/cira",
    author="Axel Gard",
    author_email="axel.gard@tutanota.com",
    license="MIT",
    packages=[
        "cira",
        "cira.asset",
        "cira.strategy",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "alpaca-py==0.21.0",
        "schedule==1.2.0",
        "matplotlib",
        "pandas",
        "numpy",
    ],
    extras_require={
        'dev': [
            'pytest',
            "black",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
