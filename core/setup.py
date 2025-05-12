from setuptools import setup, find_packages
from core import __version__
setup(
    name="nexusforge-core",
    version=f"{__version__}",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.9",
)