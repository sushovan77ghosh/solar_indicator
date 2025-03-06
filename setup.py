from setuptools import setup, find_packages

setup(
    name="solar_indicator",
    version="0.1.0",
    description="Solar energy indicators for PV potential and resource assessment",
    author="Sushovan Ghosh",
    author_email="sushovan.ghosh@bsc.es",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "xarray",
        "numpy",
        "netCDF4",
    ],
)

