# high-frequency-trading

[![high-frequency-trading](https://github.com/skosachiov/high-frequency-trading/actions/workflows/main.yml/badge.svg)](https://github.com/skosachiov/high-frequency-trading/actions/workflows/main.yml)

A small devops project can be used as a template for organizing a python-kafka-clickhouse performance testing system. In this case, high-frequency trading systems.

Python script generates data at 1ms interval, Kafka and Clickhouse try to broadcast, collect and process this data.

Since the system depends on many factors, a CI/CD process is built that constantly tests the performance of the components. Build-test-deploy cycle. Testing is built around a docker-compose file as the simplest basis.

## Data path

Data path: `Python generator` -> `Kafka` -> `Clickhouse` -> `Web` -> `Triggers`.

### Python generator

- The time_ns function was used for generation
- Container with python 3.11 - they say that sleep in 3.11 is implemented better
- Kafka producer receives json.dump
- If the generator failed to sleep 100 cycles in a row - there is a logging.critical("overload") alarm

### Kafka

Kafka is configured by default and requires Zookieper to work.

### Clickhouse

Data is transferred from the queue to the database using MATERIALIZED VIEW On the clickhouse side. Monitoring is based on the still experimental Clickhouse LIVE VIEW and curl feature.

### Web

`echo 'WATCH hft.monitoring' | curl 'http://localhost:8123/?allow_experimental_live_view=1' --data-binary @-`

We believe that when receiving 2 events, the testing was successful.
`echo 'WATCH hft.monitoring LIMIT 2' | curl -s 'http://localhost:8123/?allow_experimental_live_view=1' --data-binary @-`

### Triggers

Not yet included in the project.

## CI/CD without Github Actions and Jenkins

To develop on a local computer in the style of CI / CD without Github Actions and Jenkins, you need to install ubuntu-22.04 (also on github) in a virtual machine, after which you can use the docker-compose profiles:
- `git clone git@github.com:skosachiov/high-frequency-trading.git`
- `cd high-frequency-trading`
- `sudo docker-compose --profile build up`. Need to get "Ran 2 tests in 0.584s OK"
- `sudo docker-compose --profile test up`. You can start monitoring in another session: <br/>
`user@ubuntu:~$ echo 'WATCH hft.monitoring' | curl 'http://localhost:8123/?allow_experimental_live_view=1' --data-binary @-`
- If everything is OK, deploy: `sudo docker-compose --profile deploy up -d`

## Useful commands for local development with docker-compose

`git commit -a -m "some fix"; git push`

`git pull; sudo docker-compose --profile test up [-d]`

`DEBUG="" python -u hft_producer.py 6000 0.01 10`

