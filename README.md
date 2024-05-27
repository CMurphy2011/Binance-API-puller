# Binance-API-puller
Small fragment of a larger project. This showcases a chaining of requests in order to obtain 7 days worth of data from the Binance REST API, which then outputs a CSV. Usually, the Binance API can only support up to 1500 requests, which on intervals smaller than 10 minutes, exceeds that number for a week.
