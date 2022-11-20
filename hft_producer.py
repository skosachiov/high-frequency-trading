import logging
import time
import random
import math
import sys
import os
import json
from kafka import KafkaProducer


def hft_dataset(n_prices):
    """Trade dataset generator"""
    d = {}
    avg = {}
    d['ts'] = int(round(time.time_ns()/1e6))
    d['prices_keys'] = []
    d['prices_values'] = []
    for t in ['bid', 'ask']:
        avg[t] = 0
        for i in range(1, n_prices + 1):
            r = 1 + random.random() * (i*10 - 1)
            d['prices_keys'] += [t + '_' + str(i).zfill(2)]
            d['prices_values'] += [r]
            avg[t] += r
    d['stats_keys'] = ["bid_avg", "ask_avg"]
    d['stats_values'] = [avg['bid']/n_prices, avg['ask']/n_prices]

    assert len(d) + len(d['prices_keys']) == 5 + n_prices*2, \
        f"Wrong dict size, waiting {5 + n_prices*2}, got {len(d) + len(d['prices_keys'])}"
    assert 1 <= d['prices_values'][0] and d['prices_values'][0] <= 10, \
        f"Wrong first element, out of range 1..10"
    return d

def hft_datastream(max_iter, interval, n_prices, producer = None, topic = None):
    """High frequency trade datastream generator"""
    start_time = math.ceil(time.time())
    for i in range(1, max_iter):
        d = hft_dataset(n_prices)
        producer.send(topic, d)
        sleep_duration = start_time + i*interval - time.time_ns()/1e9
        if sleep_duration < 0:
            logging.critical("Generation process overload")
        else:
            time.sleep(sleep_duration)
    return i


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.WARNING)
    if "DEBUG" in os.environ: logging.getLogger().setLevel(logging.DEBUG)
    if "INFO" in os.environ: logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) < 4:
        logging.warning("Arguments must be specified: " +
            sys.argv[0] + " max_iter interval n_prices [kafka_host:port]")
        exit(1)
    elif len(sys.argv) == 4:
        hft_datastream(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
    else:
        bootstrap_servers = [sys.argv[4]]
        topic = 'hft_topic'
        producer = KafkaProducer(bootstrap_servers = bootstrap_servers,
            value_serializer = lambda v: json.dumps(v).encode('utf-8'))
        hft_datastream(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), producer, topic)
        producer.close()
