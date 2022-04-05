# Store Shop Instruction

## Change .env file

```yaml
POSTGRES_NAME='<>'
POSTGRES_USER='<>'
POSTGRES_PASSWORD='<>'
POSTGRES_HOST='<>'
POSTGRES_PORT=5432
```

## Build project:
```yaml
docker-compose up --build
```

## If does not exists database then need create has he with the help of commands:
```yaml
docker exec -it your_container_name psql -U postgres -c "CREATE DATABASE mydatabase;"
docker exec -it your_container_name psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;"
```

## Run project after build:
```yaml
docker-compose up
```