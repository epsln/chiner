from setuptools import setup, find_packages

setup(
        name="chiner",
        version="0.1",
        description="Playlist creator using autoencoder",
        author="epsil0n",
        package_dir = {"": "src"},
        packages = find_packages("src")
        )
