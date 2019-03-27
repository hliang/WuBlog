from setuptools import find_packages, setup

setup(
    name="wublog",
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

# To include other files, such as the static and templates directories,
# include_package_data is set. Python needs another file named MANIFEST.in
# to tell what this other data is.
