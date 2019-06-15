import setuptools

version = "0.1"

setuptools.setup(
    name="comfy",
    packages=setuptools.find_packages(),
    description="Python library for parsing config files with typed schemata",
    author="TrustYou",
    author_email="development@trustyou.com",
    version=version,
    url="https://github.com/trustyou/comfy",
    install_requires=[
        'typing;python_version<"3.5"'
    ],
    include_package_data=True,
    package_data={'comfy': ['py.typed']},
)
