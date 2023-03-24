# Analytics REST API

This REST API will provide analytics for a given day.

## To run the application

### 1. System Requirements

- Python 3.8
- pip3

### 2. Install Requirements

```shell
make setup
```

### 3. Run the application

To load to database, `DATA_DIR` ENV is expected to set. Otherwise, it will be ignored.
The repo includes sample data.

```shell
export DATA_DIR=./sample-data
```

Run the app
```shell
make run
```

#### Sample cURL request
```shell
curl --location 'http://localhost:5000/analytics' \
--header 'Content-Type: application/json' \
--data '{
    "day":"2019-08-01"
}'
```

#### Output
```json
{
    "customers": 9,
    "items": 2895
}
```

## Local development

#### Useful commands

| **Command**               | **Description**                       |
|---------------------------|---------------------------------------|
| ``` make setup-dev ```    | Install requirements                  |
| ``` make check_format ``` | Check which files will be reformatted |
| ``` make format ```       | Format files                          |
| ``` make lint ```         | Lint checks                           |
| ``` make test-unit ```    | Run unit tests                        |
| ``` make clean-app ```    | Clean app                             |

Note: Check [Makefile](Makefile) for more commands


