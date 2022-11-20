CREATE DATABASE IF NOT EXISTS hft;

CREATE TABLE IF NOT EXISTS hft.kafka (
    ts DateTime64(3),
    prices_keys Array(String),
    prices_values Array(Float64),
    stats_keys Array(String),
    stats_values Array(Float64)
)
ENGINE = Kafka('{{KAFKA_HOST}}:9092', 'hft_topic', 'clickhouse', 'JSONEachRow');

CREATE TABLE IF NOT EXISTS hft.data (
    ts DateTime64(3),
    prices_keys Array(String),
    prices_values Array(Float64),
    stats_keys Array(String),
    stats_values Array(Float64)
)
ENGINE = MergeTree()
ORDER BY ts;

CREATE MATERIALIZED VIEW hft.consumer TO hft.data AS SELECT * FROM hft.kafka;
