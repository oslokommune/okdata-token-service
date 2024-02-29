import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="okdata-token-service",
    version="0.0.1",
    author="Origo Dataplattform",
    author_email="dataplattform@oslo.kommune.no",
    description="Api for creating access tokens for users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-token-service",
    packages=setuptools.find_packages(),
    install_requires=[
        "aws-xray-sdk>=2.12,<3",
        "jsonschema",
        "okdata-aws>=2,<3",
        "python-keycloak>=1,<2",
    ],
)
