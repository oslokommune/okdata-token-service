import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="token-service",
    version="0.0.1",
    author="Origo Dataplattform",
    author_email="dataplattform@oslo.kommune.no",
    description="Api for creating access tokens for users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.oslo.kommune.no/origo-dataplatform/token-service",
    packages=setuptools.find_packages(),
    install_requires=["jsonschema", "dataplatform-common-python==0.3.0"],
)
