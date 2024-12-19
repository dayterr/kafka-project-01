# kafka-project-01

## Шаг 1
команда:
`docker-compose up`

## Шаг 2
команда:
```
docker exec -it kafka-project-01-kafka-0-1 kafka-topics.sh --create --topic  test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 2
```

