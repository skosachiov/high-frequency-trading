# high-frequency-trading

[![high-frequency-trading](https://github.com/skosachiov/high-frequency-trading/actions/workflows/main.yml/badge.svg)](https://github.com/skosachiov/high-frequency-trading/actions/workflows/main.yml)

A small devops project can be used as a template for organizing a python-kafka-clickhouse performance testing system. In this case, high-frequency trading systems.

Python script generates data at 1ms interval, Kafka and Clickhouse try to broadcast, collect and process this data.

Since the system depends on many factors, a CI/CD process is built that constantly tests the performance of the components. Build-test-deploy cycle. Testing is built around a docker-compose file as the simplest basis.

Data path: `Python generator` -> `Kafka` -> `Clickhouse` -> `Web` -> `Triggers`.

## Data path

### Python generator

### Kafka

### Clickhouse

### Web

`echo 'WATCH hft.monitoring' | curl 'http://localhost:8123/?allow_experimental_live_view=1' --data-binary @-`

We believe that when receiving 5 events, the testing was successful.
`echo 'WATCH hft.monitoring LIMIT 5' | curl 'http://localhost:8123/?allow_experimental_live_view=1' --data-binary @-`

### Triggers

Not yet included in the project.

## Useful commands for local development with docker-compose

`git commit -a -m "some fix"; git push`

`git pull; sudo docker-compose --profile test up`

`DEBUG="" python -u hft_producer.py 6000 0.01 10 kafka_test:9092`

