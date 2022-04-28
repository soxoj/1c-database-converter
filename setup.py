from setuptools import setup, find_packages

exec(open('onec_database_converter/_version.py').read())

with open('requirements.txt') as rf:
    requires = rf.read().splitlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="onec_database_converter",
    version=__version__,
    description="A skeleton for OSINT CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soxoj/osint-cli-tool-skeleton",
    author="Soxoj",
    author_email="soxoj@protonmail.com",
    entry_points={'console_scripts': ['onec_database_converter = onec_database_converter.__init__:run']},
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
