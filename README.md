# user-management

Step to setup the project

- Install pipx
  `brew install pipx`
- Verify pipx using command ensurepath
  `pipx ensurepath`
- Install poetry
  `pipx install poetry`
- init poetry at the parent directory
  `poetry init`
- Add fastAPI
  `poetry add fastapi click uvicorn alembic sqlalchemy geoalchemy2 asyncpg`

Local run
`poetry export --without-hashes -f requirements.txt -o requirements.txt`
`python3 -m venv venv && . venv/bin/activate`
`pip install --no-cache-dir --no-deps -r requirements.txt`

### Docker build

```
docker-compose build
docker-compose up
```

### Init alembic

```
docker exec -it user-management-backend alembic init -t async db/alembic
```

### Edit file

- alembic.ini
  `sqlalchemy.url = postgresql+asyncpg://postgres:postgres@user-management-postgres:5432/user_mgt`
- alembic/env.py

```
from database import Base
from models import User

# Change target_metadata to: 
target_metadata = Base.metadata


def include_name(name, type_, parent_names):
   if type_ == "schema":
     return False
   else:
     return True
     
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_name=include_name, # added
    )

    with context.begin_transaction():
        context.run_migrations()
```

- Create revision model and actual tables in database

```
docker exec -it user-management-backend /bin/bash -c "cd db && alembic revision --autogenerate -m 'create models'"
docker exec -it user-management-backend /bin/bash -c "cd db && alembic upgrade head"
```

### Convention

- SQL table, column naming
  https://www.sqlshack.com/learn-sql-naming-conventions/

### References

- Datetime insertion
  https://stackoverflow.com/questions/75363733/sqlalchemy-2-0-orm-model-datetime-insertion

- Documenting
  https://realpython.com/documenting-python-code/#commenting-code-via-type-hinting-python-35

- POST, PUT, PATCH discussion
  https://stackoverflow.com/questions/31089221/what-is-the-difference-between-put-post-and-patch

- SQL Join children
  https://www.geeksforgeeks.org/sqlalchemy-group-by-with-full-child-objects/

- Commit(persistently execute) vs flush(leniently execute)
  https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit