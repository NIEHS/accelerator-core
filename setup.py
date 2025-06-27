from setuptools import setup, find_packages

setup(
    name="accelerator_core",
    version="0.1.0",
    description="Core libraries for the accelerator metadata backbone",
    author="Mike Conway",
    author_email="mike.conway@nih.gov",
    url="https://github.com/yourusername/accelerator-core",
    packages=find_packages(),
    install_requires=[open("requirements.txt").read()],
    license="BSD 3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    package_data={
        "accelerator_core": [
            "schema/templates/*.jinja",
            "schema/type_matrix.yaml",
            "schema/*.json",
        ]
    },
    include_package_data=True,
)
