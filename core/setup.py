from setuptools import setup, find_packages

setup(
    name="nexusforge-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.9",
)