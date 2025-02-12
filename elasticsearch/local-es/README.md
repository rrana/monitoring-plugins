### Build and Start the Container

```
docker-compose up --build -d
```

##  Verify Elasticsearch is Running
```
curl -X GET http://localhost/_cluster/health?pretty
```

## Create a Sample Index
```
curl -X PUT "http://localhost/sample-index" -H 'Content-Type: application/json' -d '{
  "settings": { "number_of_shards": 1, "number_of_replicas": 1 },
  "mappings": { "properties": { "name": { "type": "text" } } }
}'
```

## Insert Sample Data
```
curl -X POST "http://localhost/sample-index/_doc/1" -H 'Content-Type: application/json' -d '{
  "name": "Test Document"
}'
```

## Query the Index
```
curl -X GET "http://localhost/sample-index/_search?pretty"
```

## Stop and Remove the Container
```
docker-compose down
```
