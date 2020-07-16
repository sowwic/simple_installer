import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dsInstaller",
    version="0.1.2",
    author="Dmitrii Shevchenko",
    author_email="dmitrii.shevchenko96@gmail.com",
    decription="Simple zip package installer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/S0nic014/dsInstaller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
