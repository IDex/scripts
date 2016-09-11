from setuptools import setup, find_packages
setup(
    name = "redshiftplus",
    version = "0.2",
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "rsp= redshiftplus.redshiftplus:main",
        ]
    }
)
