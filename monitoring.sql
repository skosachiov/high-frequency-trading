SET allow_experimental_live_view = 1;

CREATE LIVE VIEW hft.monitoring AS
SELECT ts
FROM hft.data
WHERE (prices_values[indexOf(prices_keys, 'ask_01')] +
    prices_values[indexOf(prices_keys, 'bid_01')])/2 > 9.9;

