# Full Fibre Back-End Technical Test API Template

This application is a template Flask RESTful API for back-end technical tests for Full Fibre

### Setup
This application requires Python 3.8

To run this application, simply run the `run.py` file, this will serve the API on `localhost:5000/api/v1.0`. Swagger documentation is automatically provided for all endpoints by visiting this URL. 

You will need create virtual environment in python and install the libraries listed in the requirements.txt. To do this you can run the following commands:

```shell script
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
deactivate
```

### Usage

You do not need to do anything specific to register a namespace for this API, this step has already been completed for you. 
The main two files you will be working with are `appointments_endpoint.py` and `appointments_resources.py`, these files handle endpoint definitions and endpoint execution code respectively.

You will be interfacing with a SQLite3 database (`technical_test.db`) for this test, which mirrors the same schema found in the ERD in the previous section. Some data has been provided for some tables, however most tables are empty, you may use whatever test data you wish.

The `appointments_resources.py` file has a pre-defined variable called `self.DB`, which is an instance of the `DatabaseConnection` class found in `db.py`. This class has the following methods which you can use to interface with the database
- `select(query: str)`
- `insert(query: str, expect_return: bool = False)`
- `update(query: str, expect_return: bool = False)`
- `delete(query: str)`

Methods which have the optional `expect_return` parameter will return the result of `cursor.fetchall()` if the parameter is set. `select` always returns the result.

Data returned by these methods will be in the form of an array of dictionaries, with the column names added as labels to the data to make it easier to use.

If you wish to reset the database, you can run the `database_setup.py` file, which will set the database to the same state as when you received this test.