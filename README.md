# PyCDS Alembic Client

This project provides a template for using 
[PyCDS](https://github.com/pacificclimate/pycds) 
to set up a migrated database
suitable for testing. The method is straightforward, and is encapsulated
in the fixtures `alembic_script_location` and `pycds_engine` in 
`tests/conftest.py`. A test which uses these fixtures is provided in 
`tests/test_database.py`.

For the curious, the method for getting access to an installed package (here,
PyCDS) as a filesystem is detailed in 
[Example 5 of the `resources-example` project ](https://github.com/wimglenn/resources-example/blob/master/myapp/example5.py).
Such access is required to run the Alembic migrations from the test code.
