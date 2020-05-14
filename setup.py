from setuptools import setup, find_packages

# version information
MAJOR = 1
MINOR = 0
MICRO = 0
PRERELEASE = 0
ISRELEASED = True
version = "{}.{}.{}".format(MAJOR, MINOR, MICRO)

if not ISRELEASED:
    version += ".dev{}".format(PRERELEASE)

# write version information to file

def write_version_file(version):
    "writes version file that is read when importing version number"
    version_file = """'''
Version file automatically created by setup.py file
'''
version = '{}'
    """.format(version)

    with open("catalogue/version.py", "w") as fh:
        fh.write(version_file)

write_version_file(version)

# Source dependencies from requirements.txt file.
try:
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        install_packages = [line.strip() for line in lines]
except FileNotFoundError:
    install_packages = []

setup(
    name="repro-catalogue",
    version=version,
    install_requires=install_packages,
    include_package_data=True,
    python_requires=">=3.6",
    author='The Alan Turing Institute Research Engineering Group',
    author_email="hut23@turing.ac.uk",
    url="https://github.com/alan-turing-institute/repro-catalogue",
    # this should be a whitespace separated string of keywords, not a list
    keywords="cli-tool management version-control hashing",
    description="Tool for reproducible analyses",
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    use_package_data=True,
    entry_points={
        "console_scripts": ["catalogue = catalogue.parser:main"]
    },
)
