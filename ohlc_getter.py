import pandas as pd
from datetime import datetime, timedelta
import requests

binance_api_base_url = 'https://fapi.binance.com'


def get_binance_candlestick_data_7_day(symbol):
    interval = '5m'  # INTERVAL
    end_time_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # CURRENT DATE AND TIME
    end_time = datetime.strptime(end_time_input, "%Y-%m-%d %H:%M:%S")
    start_time = end_time - timedelta(days=7)  # LOOKBACK TIME, DO NOT CHANGE
    endpoint = f'{binance_api_base_url}/fapi/v1/klines'

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1500,
        'startTime': int(start_time.timestamp() * 1000)
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    df_1 = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 516,
        'endTime': int(end_time.timestamp() * 1000)
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    df_2 = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                       'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                       'taker_buy_quote_asset_volume', 'ignore'])

    df = pd.concat([df_1, df_2])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Drop columns after 'volume'
    df = df.loc[:, :'volume']
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')

    # Add a new column called 'HL Average' calculated as the average of 'high' and 'low'
    df['HL Average'] = (df['high'] + df['low']) / 2

    df = df[['timestamp', 'open', 'high', 'low', 'close', 'HL Average', 'volume']]

    start_time_filename = start_time.strftime("%Y-%m-%d_%H-%M")
    end_time_filename = end_time.strftime("%Y-%m-%d_%H-%M")

    print(df)

    return df


def get_ohlc(symbol, filename):
    candlesticks = get_binance_candlestick_data_7_day(symbol)
    candlesticks.to_csv(filename, index=False)
    print(f"Saved at {datetime.now()} !")
