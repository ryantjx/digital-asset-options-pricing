# import asyncio
# import pandas as pd
# import numpy as np
# import time
# from scipy.stats import norm
# from scipy.optimize import brentq
# from datetime import datetime, timedelta
# import pytz

# from .data.websocket.websocket_api import DeribitWebSocket
# from .DataHandler import DataHandler

# class DeribitDataHandler(DataHandler):
#     def __init__(self, postgresql_hostname, postgresql_database, postgresql_username, postgresql_port, dynamodb_regionname, handler_logger) -> None:
#         super().__init__(postgresql_hostname, postgresql_database, postgresql_username, postgresql_port, dynamodb_regionname, handler_logger)
#         self.deribit_api = DeribitWebSocket()

#     """
#     Overriden Functions
#     """
#     def refresh_map(self):
#         return super().refresh_map(platform_datasource_name="deribit")
    
#     def update_database(self):
#         self.refresh_map()
#         tasks = []
#         update_handlers = {
#             # 'binance' : {
#             #         'binance': {
#             #         'SPOT': self.update_Binance_SPOT,
#             #         'USDMPERP': self.update_binance_USDM,
#             #     },
#             # },
#             'deribit': {
#                 'deribit': {
#                     'option' : self.async_update_deribit,
#                 },
#             },
#             # 'coinalyze' : {
#             #     'coinalyze': {
#             #         '_PERP.A' : self.update_coinalyze_perp,
#             #         'PERP_ALL_ALTS' : self.update_coinalyze_all_perp,
#             #         'PERP_ALL_BTC' : self.update_coinalyze_all_perp,
#             #         'PERP_ALL_ETH' : self.update_coinalyze_all_perp,
#             #     },
#             # }
#         }
#         for symbol_id, symbol_params in self.symbol_map.items():
#             if symbol_params['is_active'] == False:
#                 print(f"Symbol ID {symbol_id} is not active. ")
#                 continue
#             platform_datasource = symbol_params['platform_datasource_name']
#             platform = symbol_params['platform_name']
#             contract_name = symbol_params['contract_name']
#             update_func = update_handlers.get(platform_datasource, {}).get(platform, {}).get(contract_name)
#             if update_func:
#                 # print(self._format_instrument_string(platform, symbol_params))
#                 # update_func(symbol_id)
#                 if asyncio.iscoroutinefunction(update_func):
#                     tasks.append(update_func(symbol_id))
#                 else:
#                     update_func(symbol_id)
#             else:
#                 print(f"ERROR: Contract Name {contract_name} not supported for {platform}")
#         # If there are any async tasks, run them all together
#         if tasks:
#             asyncio.run(self.execute_async_tasks(tasks))

#     async def deribit_add_option_instruments(self, symbol_id):
#         # margin_currency == counter_currency in this context
#         # Currently only 29 - 33 is deribit data
#         try:
#             symbol_params = self.symbol_map.get(symbol_id)
#             if symbol_params is None:
#                 raise ValueError(f"Symbol ID {symbol_id} not found in symbol_map.")
            
#             currency = symbol_params['quote_currency']
#             instrument = symbol_params['contract_name']
#             db_instrument_ids = [row[0] for row in self.postgresql_db.execute_query_fetchall(f"""SELECT DISTINCT instrument_id FROM deribit_instruments WHERE symbol_id = {symbol_id};""")]
            
#             active_options = await self.deribit_api.callWebSocket("public/get_instruments", {"currency": currency, "kind": instrument, "expired": False})
            
#             key_columns = [
#                 'instrument_id',
#                 'instrument_name',
#                 'instrument_type',
#                 'option_type',
#                 'kind', 
#                 'strike',
#                 'contract_size',
#                 'base_currency', 
#                 'quote_currency', 
#                 'counter_currency',
#                 'price_index',
#                 'is_active',
#                 'settlement_period',
#                 'settlement_currency',
#                 'expiration_timestamp',
#                 'rfq'
#             ]
            
#             df_instruments = pd.DataFrame(active_options)
            
#             # Filter for key columns
#             filtered_df = df_instruments.reindex(columns=key_columns)
#             filtered_df = filtered_df.where(pd.notnull(filtered_df), None)
#             # Filter for existing instruments
#             filtered_df = filtered_df[~filtered_df['instrument_id'].isin(db_instrument_ids)]
            
#             # Insert new ids
#             max_id_query = "SELECT MAX(deribit_instruments_id) FROM deribit_instruments;"
#             max_id_result = self.postgresql_db.execute_query_fetchone(max_id_query)
#             max_id = max_id_result[0] if max_id_result[0] is not None else 0
#             new_ids = [max_id + i + 1 for i in range(len(filtered_df))]
#             filtered_df.insert(0, 'deribit_instruments_id', new_ids)
#             filtered_df.insert(1, 'symbol_id', symbol_id)
#             filtered_df['style'] = 'european'
            
#             self.postgresql_db.bulk_insert_dataframe(filtered_df, 'deribit_instruments')
#             self.handler_logger.logger.info(f"Deribit Instruments Success - Symbol ID {symbol_id}.")
#         except Exception as e:
#             self.handler_logger.logger.error(f"Deribit Instruments Error - Symbol ID {symbol_id} - {e}.")

#     async def update_deribit_market_data(self, symbol_id):
#         try:
#             current_timestamp = int(datetime.now(pytz.UTC).timestamp() * 1000)
#             instruments = self.postgresql_db.execute_query_fetchall(f"""SELECT instrument_name, price_index, strike, expiration_timestamp, deribit_instruments_id FROM deribit_instruments WHERE symbol_id = {symbol_id} AND expiration_timestamp > {current_timestamp};""")
#             options_data = []
#             index = 0
#             while index < len(instruments):
#                 response = await self.deribit_api.callWebSocket("public/get_book_summary_by_instrument", {"instrument_name": instruments[index][0]})
#                 time.sleep(0.1)
#                 if type(response[0]) == dict:
#                     data = response[0]
#                     data['price_index'] = instruments[index][1]
#                     data['strike'] = float(instruments[index][2])
#                     data['expiration_timestamp'] = int(instruments[index][3])
#                     data['deribit_instruments_id'] = instruments[index][4]
#                     options_data.append(data)
#                     index += 1
#                 else:
#                     print(f"Querying for {instruments[index][0]} again.")
#             df_instruments = pd.DataFrame(options_data)
#             df_instruments.loc[:,'timestamp'] = current_timestamp
#             df_instruments.loc[:,'creation_datetime'] = pd.to_datetime(df_instruments['creation_timestamp'], unit='ms', utc=True)
#             df_instruments.loc[:,'expiration_datetime'] = pd.to_datetime(df_instruments['expiration_timestamp'], unit='ms', utc=True)
#             df_instruments.loc[:,"option_type"] = df_instruments['instrument_name'].str.split("-").str[-1].map(lambda x: "call" if "C" in x else "put")
#             df_instruments.loc[:,'timestamp_to_expiry'] = df_instruments['expiration_timestamp'] - current_timestamp

#             # Time to expiry is in a year
#             df_instruments.loc[:,'year_to_expiry'] = (df_instruments['expiration_timestamp'] - current_timestamp) / (60*60*24*365.25*1000)
#             df_instruments.loc[:,"forward_price"] = df_instruments['underlying_price'] * np.exp(df_instruments['interest_rate'] * df_instruments['year_to_expiry'])
#             df_instruments.loc[:,"log_simple_moneyness"] = np.log(df_instruments['strike'] / df_instruments['forward_price'])

#             def EuropeanBSMCallValue(S, K, r, T, d1, d2):
#                 """
#                 Returns the theoretical value of a European call option according to the BSM model.
#                 Parameters:
#                     S (float) : The current price of the underlying asset
#                     K (float) : The strike price of the option
#                     r (float) : The risk-free interest rate
#                     T (float) : The time to expiry in years
#                     d1 (float) : The D1 term in the BSM call value formula
#                     d2 (float) : The D2 term in the BSM call value formula
#                 Returns:
#                     float : The theoretical value of the call option
#                 """
#                 bsm_call_value = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
#                 return bsm_call_value

#             def EuropeanBSMPutValue(S, K, r, T, d1, d2):
#                 """
#                 Returns the theoretical value of a European put option according to the BSM model.
#                 Parameters:
#                     S (float) : The current price of the underlying asset
#                     K (float) : The strike price of the option
#                     r (float) : The risk-free interest rate
#                     T (float) : The time to expiry in years
#                     d1 (float) : The D1 term in the BSM put value formula
#                     d2 (float) : The D2 term in the BSM put value formula
#                 Returns:
#                     float : The theoretical value of the put option
#                 """
#                 bsm_put_value = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)
#                 return bsm_put_value

#             def calculate_d1(S, K, T, r, sigma):
#                 return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

#             def calculate_d2(d1, sigma, T):
#                 return d1 - sigma * np.sqrt(T)

#             # Objective function for IV calculation
#             def iv_objective(sigma, market_price, S, K, r, T, option_type):
#                 d1 = calculate_d1(S, K, T, r, sigma)
#                 d2 = calculate_d2(d1, sigma, T)
#                 if option_type == 'call':
#                     return EuropeanBSMCallValue(S, K, r, T, d1, d2) - market_price
#                 else:  # 'put'
#                     return EuropeanBSMPutValue(S, K, r, T, d1, d2) - market_price

#             def find_iv(S, K, T, r, market_price, option_type):
#                 """
#                 Solve for the implied volatility of an option given a row of the DataFrame.
#                 """

#                 # Provide an initial bracket [0.0001, 5] for the IV values
#                 try:
#                     iv = brentq(iv_objective, -1, 5, args=(market_price, S, K, r, T, option_type))
#                     if iv < 0:
#                         iv = 0.0001
#                 except ValueError:
#                     iv = np.nan  # Use NaN for options where IV couldn't be calculated
#                 return iv

#             def delta(S, K, T, r, sigma, option_type="call"):
#                 d1 = calculate_d1(S=S, K=K, T=T, r=r, sigma=sigma)
#                 if option_type == "call":
#                     return norm.cdf(d1, 0, 1)
#                 else:
#                     return -norm.cdf(-d1, 0, 1)
#             def gamma(S, K, T, r, sigma):
#                 d1 = calculate_d1(S=S, K=K, T=T, r=r, sigma=sigma)
#                 return norm.pdf(d1, 0, 1) / (S * sigma * np.sqrt(T))
#             def vega(S, K, T, r, sigma):
#                 d1 = calculate_d1(S=S, K=K, T=T, r=r, sigma=sigma)
#                 return S * norm.pdf(d1, 0, 1) * np.sqrt(T) / 100

#             def theta(S, K, T, r, sigma, option_type = "call"):
#                 d1 = calculate_d1(S=S, K=K, T=T, r=r, sigma=sigma)
#                 d2 = calculate_d2(d1, sigma, T)
#                 if option_type == "call":
#                     return -S * norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
#                 else:
#                     return -S * norm.pdf(d1, 0, 1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2, 0, 1)

#             def expected_move(S, sigma, T):
#                 return S * sigma * np.sqrt(T)

#             df_instruments['implied_volatility'] = df_instruments.apply(lambda row: find_iv(S=row['underlying_price'], 
#                                                                                         K=row['strike'], 
#                                                                                         T=row['year_to_expiry'], 
#                                                                                         r=row['interest_rate'], 
#                                                                                         market_price=row['mark_price'], 
#                                                                                         option_type=row['option_type']), axis=1)
#             df_instruments['delta'] = df_instruments.apply(lambda row: delta(S=row['underlying_price'], 
#                                                                                     K=row['strike'], 
#                                                                                     T=row['year_to_expiry'], 
#                                                                                     r=row['interest_rate'], 
#                                                                                     sigma=row['implied_volatility'], 
#                                                                                     option_type = row['option_type']), axis=1)
#             df_instruments['gamma'] = df_instruments.apply(lambda row: gamma(S=row['underlying_price'], 
#                                                                                     K=row['strike'], 
#                                                                                     T=row['year_to_expiry'], 
#                                                                                     r=row['interest_rate'], 
#                                                                                     sigma=row['implied_volatility']), axis=1)
#             df_instruments['vega'] = df_instruments.apply(lambda row: vega(S=row['underlying_price'], 
#                                                                                 K=row['strike'], 
#                                                                                 T=row['year_to_expiry'], 
#                                                                                 r=row['interest_rate'], 
#                                                                                 sigma=row['implied_volatility']), axis=1)
#             df_instruments['theta'] = df_instruments.apply(lambda row: theta(S=row['underlying_price'], 
#                                                                                     K=row['strike'], 
#                                                                                     T=row['year_to_expiry'], 
#                                                                                     r=row['interest_rate'],
#                                                                                     sigma= row['implied_volatility'],
#                                                                                     option_type=row['option_type']), axis=1)
#             df_instruments['expected_move'] = df_instruments.apply(lambda row: expected_move(S=row['underlying_price'], 
#                                                                                                     sigma=row['implied_volatility'], 
#                                                                                                     T=row['year_to_expiry']), axis=1)
#             market_data_columns = ['deribit_instruments_id', 'timestamp', 'timestamp_to_expiry',
#                             'underlying_price', 'underlying_index', 'mark_price', 'bid_price', 'ask_price', 'mid_price', 'low', 'last', 'high', 
#                             'open_interest','interest_rate', 'volume', 'volume_usd','volume_notional', 'price_change', 
#                             'estimated_delivery_price', 'current_funding', 'funding_8h', 'forward_price', 'log_simple_moneyness', 'implied_volatility',
#                             'delta', 'gamma', 'theta', 'vega', 'expected_move']

#             # Filter for key columns
#             filtered_df = df_instruments.reindex(columns=market_data_columns)
#             filtered_df = filtered_df.where(pd.notnull(filtered_df), None)
#             exclude_columns = [
#             'underlying_index','deribit_instruments_id', 'timestamp', 'timestamp_to_expiry'
#             ]
#             # Automatically exclude additional integer columns
#             for col in filtered_df.columns:
#                 if filtered_df[col].dtype in ['int64', 'bigint']:  # Adjust 'bigint' if your DataFrame uses a different designation
#                     exclude_columns.append(col)

#             # Convert the remaining columns to float, except those explicitly excluded
#             for col in filtered_df.columns:
#                 if col not in exclude_columns:
#                     filtered_df[col] = filtered_df[col].astype('float64')

#             self.postgresql_db.bulk_insert_dataframe(filtered_df, 'deribit_market_data')
#             self.handler_logger.logger.info(f"Deribit Market Data Success - Symbol ID {symbol_id}.")
#         except Exception as e:
#             self.handler_logger.logger.error(f"Deribit Market Data Error - Symbol ID {symbol_id} - {e}.")

#     async def update_deribit_orderbook_data(self, symbol_id):
#         try:
#             current_timestamp = int(datetime.now(pytz.UTC).timestamp() * 1000)
#             instruments = self.postgresql_db.execute_query_fetchall(f"""SELECT deribit_instruments_id, instrument_id FROM deribit_instruments WHERE symbol_id = {symbol_id} AND expiration_timestamp > {current_timestamp};""")
#             orderbook_data = []
#             index = 0
#             while index < len(instruments):
#                 response = await self.deribit_api.callWebSocket("public/get_order_book_by_instrument_id", {"instrument_id": instruments[index][1], "depth": 1})
#                 time.sleep(0.1)
#                 if type(response) == dict:
#                     response['deribit_instruments_id'] = instruments[index][0]
#                     response['delta'] = response['greeks']['delta']
#                     response['gamma'] = response['greeks']['gamma']
#                     response['theta'] = response['greeks']['theta']
#                     response['vega'] = response['greeks']['vega']
#                     response['rho'] = response['greeks']['rho']
#                     response['volume_usd'] = response['stats']['volume_usd']
#                     response['volume'] = response['stats']['volume']
#                     response['price_change'] = response['stats']['price_change']
#                     response['low'] = response['stats']['low']
#                     response['high'] = response['stats']['high']
#                     orderbook_data.append(response)
#                     index += 1
#             orderbook_data_columns = ["deribit_instruments_id", "timestamp", "underlying_index", "underlying_price",
#                         "index_price", "instrument_name", "interest_rate", "open_interest", "max_price",
#                         "min_price", "last_price", "mark_price", "best_ask_price", "best_bid_price", "best_ask_amount",
#                         "best_bid_amount", "settlement_price", "delivery_price", "state", "high", "low",
#                         "volume", "volume_usd", "price_change", "ask_iv", "bid_iv", "mark_iv", "delta",
#                         "gamma", "theta", "vega", "rho", "current_funding", "funding_8h"
#                     ]
#             df_orderbook = pd.DataFrame(orderbook_data)
#             df_orderbook = df_orderbook.reindex(columns=orderbook_data_columns)
#             df_orderbook = df_orderbook.where(pd.notnull(df_orderbook), None)
#             exclude_columns = ["deribit_instruments_id", "underlying_index", "instrument_name", "state"]
#             for col in df_orderbook.columns:
#                 if col not in exclude_columns:
#                     df_orderbook[col] = df_orderbook[col].astype('float64')
#             self.postgresql_db.bulk_insert_dataframe(df_orderbook, 'deribit_orderbook_data')
#             self.handler_logger.logger.info(f"Deribit Orderbook Data Success - Symbol ID {symbol_id}.")
#         except Exception as e:
#             self.handler_logger.logger.error(f"Deribit Orderbook Data Error - Symbol ID {symbol_id} - {e}.")
#     async def async_update_deribit(self, symbol_id):
#         try:
#             symbol_params = self.symbol_map.get(symbol_id)
#             if symbol_params is None:
#                 print(f"Symbol ID {symbol_id} not found in symbol_map.")
#                 return
#             if symbol_id in [32, 33]:
#                 print(f"Deribit Option Instruments for symbol_id {symbol_id} defaulted to 31.")
#                 return
#             await self.deribit_add_option_instruments(symbol_id)
#             await self.update_deribit_market_data(symbol_id)
#             await self.update_deribit_orderbook_data(symbol_id=symbol_id)
#         except Exception as e:
#             self.handler_logger.logger.error(f"Deribit Error - Symbol ID {symbol_id} - {e}.")

# class DeribitWebSocket(APIWebSocket):
#     def __init__(self):
#         super().__init__()
#         nest_asyncio.apply()
#         self.url = "wss://www.deribit.com/ws/api/v2"
#         self.ssl_context = ssl.create_default_context(cafile=certifi.where())
#         self.api_method_params = {
#             "public/get_book_summary_by_currency": {"required": ["currency", ], "optional": ["kind",]},
#             "public/get_book_summary_by_instrument": {"required": ["instrument_name"], "optional": []},
#             "public/get_contract_size": {"required": ["instrument_name"], "optional": []},
#             "public/get_currencies": {"required": [], "optional": []},
#             "public/get_delivery_prices": {"required": ["index_name"], "optional": ["offset", "count"]},
#             # PERPETUALS
#             "public/get_funding_chart_data": {"required": ["instrument_name", "length"], "optional": []},  # Note: "length" could be "8h", "24h", "1m"
#             "public/get_funding_rate_history": {"required": ["instrument_name", "start_timestamp", "end_timestamp"], "optional": []},
#             "public/get_funding_rate_value": {"required": ["instrument_name", "start_timestamp", "end_timestamp"], "optional": []},
            
#             "public/get_historical_volatility": {"required": ["currency"], "optional": []},
#             "public/get_index_price": {"required": ["index_name"], "optional": []},
#             "public/get_index_price_names": {"required": [], "optional": []},
#             "public/get_instrument" : {"required": ["instrument_name"], "optional": []},
#             "public/get_instruments": {"required": ["currency", "kind"], "optional": ["expired"]},
#             "public/get_last_settlements_by_currency": {"required": ["currency"], "optional": ["type", "count", "continuation", "search_start_timestamp"]},
#             "public/get_last_settlements_by_instrument": {"required": ["instrument_name"], "optional": ["type", "count", "continuation", "search_start_timestamp"]},    
#             "public/get_last_trades_by_currency": {"required": ["currency"], "optional": ["kind", "start_id", "end_id", "start_timestamp", "end_timestamp", "count", "sorting"]},
#             "public/get_last_trades_by_currency_and_time" : {"required": ["currency", "start_timestamp", "end_timestamp"], "optional": ["kind", "count", "sorting"]},
#             "public/get_last_trades_by_instrument": {"required": ["instrument_name"], "optional": ["start_seq", "end_seq", "count", "start_timestamp", "end_timestamp", "sorting"]},
#             "public/get_last_trades_by_instrument_and_time": {"required": ["instrument_name", "start_timestamp", "end_timestamp"], "optional": ["count", "sorting"]},    
#             "public/get_mark_price_history" : {"required": ["instrument_name", "start_timestamp", "end_timestamp"], "optional": []},
#             "public/get_order_book": {"required": ["instrument_name",], "optional": ["depth"]},            
#             "public/get_order_book_by_instrument_id" : {"required": ["instrument_id", ], "optional": ["depth"]},
#             "public/get_rfqs" : {"required" : ["currency"], "optional": ["kind"]},
#             "public/get_supported_index_names" : {"required": [], "optional": ["type"]},
#             "public/get_trade_volumes" : {"required": [], "optional": ["extended"]},
#             "public/get_tradingview_chart_data" : {"required": ["instrument_name", "start_timestamp", "end_timestamp", "resolution"], "optional": []},
#             "public/get_volatility_index_data" : {"required": ["currency", "start_timestamp", "end_timestamp", "resolution"], "optional": []},
#             "public/ticker" : {"required": ["instrument_name"], "optional": []},
#         }

#     """
#     on_error, on_message, on_close and on_open will implemented in the superclass
    
#     Not needed for now since data is not streamed.
#     """
#     def on_message(self, message):
#         self.logger.info(f"Deribit data received. Message: {message}")

#     async def callWebSocket(self, method, params=None, request_id=1):
#         """
#         Generic method to make API calls to Deribit WebSocket.
        
#         :param method: The API method to be called.
#         :param params: The parameters for the API call.
#         :param request_id: The JSON RPC request ID.
#         :return: The result of the API call.
#         """
#         if method not in self.api_method_params:
#             raise ValueError(f"Method {method} is not supported or not defined in the api_method_params.")

#         # Check if all required parameters are provided
#         required_params = self.api_method_params[method]["required"]
#         if not all(param in params for param in required_params):
#             missing = [param for param in required_params if param not in params]
#             raise ValueError(f"Missing required parameters for method {method}: {missing}")

#         msg = json.dumps({
#             "jsonrpc": "2.0",
#             "method": method,
#             "id": request_id,
#             "params": params or {}
#         })
#         try:
#             async with websockets.connect(self.url, ssl=self.ssl_context) as websocket:
#                 await websocket.send(msg)
#                 response = await websocket.recv()
#                 data = json.loads(response)
#                 if 'result' in data or 'error' not in data:
#                     # print(f"SUCCESS: Deribit {method}.")
#                     return data['result']
#                 else:
#                     return f"Error: {data['error'].get('message', 'Unknown error')}"
#         except websockets.ConnectionClosed as e:
#             return f"Connection closed error: {e}"
#         except websockets.InvalidStatusCode as e:
#             return f"Invalid status code: {e}"
#         except Exception as e:
#             return f"An error occurred: {e}"