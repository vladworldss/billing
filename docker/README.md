### Docker

#### Quickstart


1. Run docker-compose
```shell script
docker-compose up -d
```

Sometimes DB running not fast enough and backend can't connect to it upon first run. 
Just restart backend container in order to fix it.
```shell script
docker-compose restart backend
```

**Billing** docs now available via [http://localhost:8000/docs](http://localhost:8000/docs).

#### Connecting To Database
```shell script
docker-compose exec db psql -U billing
```
Db credentials for local (not-in-docker) deploy:

| cred | value     |
|------|-----------|
| host | localhost |
| port | 6432 |
| user | billing |
| password | billing |
| database | billing |

### Extra
* Check docker started.
  ```shell script
  docker-compose ps
  ```
  All entries should be "healthy" (rabbitmq can showing off).


* Cleaning up all docker containers, images, volumes, etc. (for current project only).
  ```shell script
  docker-compose down --volumes --rmi local --remove-orphans
  ```

* Rebuilding single container.
  ```shell script
  docker-compose stop backend
  docker-compose up -d --build backend
  ```
* **For testing**
After all we need to apply our migrations to test DB

```shell
cd {project_dir}/src
inv db.test-migration-apply
```
```shell
python -m pytest -s tests db/tests/test_models.py
```
