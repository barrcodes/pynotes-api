# pynotes-api

This is a sample API built with fastapi and postgres. Some shortcuts have been taken here, but every effort has been made to ensure a reasonable use and deployment of such an api.

In an ideal world, the api and db would not be shared under the same project / docker configuration. But for simplicity I have a single docker-compose for both.

## getting started

### Install dependencies

```python
source env/bin/activate
pip install .
```

### Setup env

Create an .env file in the root of the project with the following. These passwords will not be stored in git. In a product environment, you would take note of your passwords, and store them securely in a password manager.

If you need to modify port numbers due to existing services running on these ports, change them here.

```bash
PG_USER=postgres
PG_PASS=your-admin-password
DB_NAME=pynotesdb
DB_USER=apiuser
DB_PASS=your-user-password
DB_PORT=5432
API_PORT=8000
```

### Launch the docker configration

```python
sudo docker-compose build
sudo docker-compose up
```

One consideration for a production-ready application would be to have a separate docker-compose.prod.yaml, preferably which uses either a separate .env.prod, or which pulls directly from secure environment variables in the ci/cd pipeline. This docker configuration would not map the local directory to a volume, and would not `--reload``.

### Initialize the api user account for pynotesdb

This will create a separate user account for the database which has least privilege relevant to a typical simple read/write API user.

```bash
python scripts/init-db.py
```

### Generate the tables

Apply the supplied alembic migration(s) to the table generated in the previous step

```bash
alembic upgrade head
```

## Use the API

There's a [postman collection](notebooks.postman_collection.json), but in case it is missing any endpoints, you can feel free to dig around in [src/routers/v1](src/routers/v1).
