# Integration Tests

Unlike the /tests directory, this testing directory contains longer running tests that utilize components of the running
development system, including Mongo and potentially Airflow.

Normal unit tests belong in the /tests directory.These tests are not included in the normal post-commit Github actions.

## Configuration

The integration tests use (by default) the MongoDB installation in [deployments](../deployments). The tests are controlled by the
configuration that can be found in [test_resources](./test_resources/application.properties).

In order to supply a password for the default mongo, you can pass in the environment variable

`ACCEL_MONGODB_PASSWORD=xxxxxx`

And this will override the application.properties file.

Alternatively, you can supply an environment variable that is the absolute path to a configuration .properties file,
like this:

```
ACCELERATOR_CONFIG=/path/to/xxx.properties
```

The password for Mongo can always be replaced via the ```ACCEL_MONGODB_PASSWORD``` env variable
