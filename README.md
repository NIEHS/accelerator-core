# accelerator-core
Core libraries and classes for accelerator metadata backbone

## Description

This project is the base python package and libraries for the core of the Accelerator Project

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI/CD](https://github.com/NIEHS/accelerator-core/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/NIEHS/accelerator-core/actions/workflows/lint-and-test.yml)

![System Whiteboard](https://github.com/user-attachments/assets/2a2b07fa-bbed-454c-9050-73eccb7cbf6c)

The project implements all of the core components (accession, dissemination) and provides abstract superclasses and supporting code for all of the source and dissemination components. Addtional tools for test development, etc can be placed here but should be incorporated into specific projects as a python import

Each source and disseination target should be developed in a separate accelerator-source-xxx or accelerator-dissemination-xxx repository


## Developer Notes

This project uses pre-commit hooks to validate code, run tests, and accomplish other tasks.

Loading the requirements.txt into your dev environment will install pre-commit, then you can set up the pre-commit
hooks by running:

```
pre-commit install
```

This should be the first thing you do when cloning this project. More docs on pre-commit are available [here](https://pre-commit.com/)

## Handy References

* MongoDB Developer Center: https://www.mongodb.com/developer/
* PyMongo: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/
* Mongo DB Commands: https://www.mongodb.com/docs/manual/reference/command/
* Mongo Airflow Hook: https://www.mongodb.com/developer/products/mongodb/mongodb-apache-airflow/
* Mongo w Airflow: https://www.mongodb.com/developer/products/mongodb/mongodb-apache-airflow/
* Custom operators (may add for our accel core stuff) - https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html#custom-operator
* Managing python and other dependencies - https://airflow.apache.org/docs/apache-airflow/2.10.5/tutorial/taskflow.html#using-the-taskflow-api-with-complex-conflicting-python-dependencies
  * https://airflow.apache.org/docs/apache-airflow/2.10.5/tutorial/taskflow.html#using-the-taskflow-api-with-complex-conflicting-python-dependencies