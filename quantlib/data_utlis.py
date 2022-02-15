import pandas as pd 
import config
from binance.client import Client
import datetime

client = Client(config.API_KEY,config.API_SECRET)

# Coin list
# coin_list = ['BTCUSDT','BTCBUSD','BNBUSDT']

coin_list = ['BTCUSDT','BTCBUSD','BNBUSDT','SLPUSDT','SOLUSDT','ETHUSDT','BUSDUSDT','ETHBUSD','XRPUSDT','SHIBUSDT','TRXUSDT','GALAUSDT','DOGEUSDT',
	'DOGEUSDT','SLPBUSD','ADAUSDT','LUNAUSDT','DOTUSDT','AVAXUSDT','SLPTRY','SHIBBUSD','ETHBTC','BETAUSDT','MATICUSDT','FTMUSDT',
	'SANDUSDT','MANAUSDT','ETCUSDT','NEARUSDT','EGLDUSDT','LUNABUSD']
"""Function to get all tickers"""
def get_tickers():
	info = client.get_all_tickers()
	
	data = []
	for i in info:
		if i['symbol'] in coin_list:
			data.append(i['symbol'])
			
	return data
"""Function to get price data of tickers"""
def get_binance_data():
	symbols = get_tickers()
	ohclvs = {}
	for symbol in symbols:
		# function to find first available datepoint of symbol
		timestamp = client._get_earliest_valid_timestamp(symbol, '1d')
		# Get all the price data from starting point onwards
		bars = client.get_historical_klines(symbol, '1d', timestamp, limit=1000)
		
		bar_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close','volume','close_time','QAV','Trades','BAV','QAV','Ignore'])
		
		#Divide by 1000 for millisecond conversion
		bar_df['date'] =bar_df['date']/1000
		# Convert unix to timestamp
		bar_df['date'] = pd.to_datetime(bar_df['date'],unit='s')
		bar_df.set_index('date', inplace=True)
		bar_df = bar_df[['open', 'high', 'low','close','volume']]
		
		bar_df['open'] = bar_df['open'].astype(float)
		bar_df['high'] = bar_df['high'].astype(float)
		bar_df['low'] = bar_df['low'].astype(float)
		bar_df['close'] = bar_df['close'].astype(float)
		bar_df['volume'] = bar_df['volume'].astype(float)
		
		

		
		ohclvs[symbol] = bar_df
	#Putting everything into singel dataframe
	df = pd.DataFrame(index= ohclvs['BTCUSDT'].index)
	df.index.name = "date"
	instruments = list(ohclvs.keys())
	for inst in instruments:
		inst_df = ohclvs[inst]
		columns = list(map(lambda x: "{} {}".format(inst, x), inst_df.columns))
		df[columns] = inst_df
	return instruments,df
def extend_dataframe(traded, df):
    # df.index = pd.Series(df.index).apply(lambda x: format_date(x))
    open_cols = list(map(lambda x: str(x) + " open", traded))
    high_cols = list(map(lambda x: str(x) + " high", traded))
    low_cols = list(map(lambda x: str(x) + " low", traded))
    close_cols = list(map(lambda x: str(x) + " close", traded))
    volume_cols = list(map(lambda x: str(x) + " volume", traded))
    historical_data = df.copy()
    historical_data = historical_data[open_cols + high_cols + low_cols + close_cols + volume_cols] #get a df with ohlcv for all traded instruments
    historical_data.fillna(method="ffill", inplace=True) #fill missing data by first forward filling data, such that [] [] [] a b c [] [] [] becomes [] [] [] a b c c c c
    historical_data.fillna(method="bfill", inplace=True) #fill missing data by backward filling data, such that [] [] [] a b c c c c becomes a a a a b c c c c
    for inst in traded:
        historical_data["{} % ret".format(inst)] = historical_data["{} close".format(inst)] / historical_data["{} close".format(inst)].shift(1) - 1 #close to close return statistic
        historical_data["{} % ret vol".format(inst)] = historical_data["{} % ret".format(inst)].rolling(25).std() #historical rolling standard deviation of returns as realised volatility proxy
        #test if stock is actively trading by using rough measure of non-zero price change from previous time step
        historical_data["{} active".format(inst)] = historical_data["{} close".format(inst)] != historical_data["{} close".format(inst)].shift(1)
    return historical_data
# def format_date(date):
#     #convert 2012-02-06 00:00:00 >> datetime.date(2012, 2, 6)
#     yymmdd = list(map(lambda x: int(float(x)), str(date).split(" ")[0].split("-")))
#     return datetime.date(yymmdd[0], yymmdd[1], yymmdd[2])

# instruments,df = get_binance_data()
# df = extend_dataframe(traded=instruments,df=df)
# df.to_csv("./price_data/stock_data_2.csv")
# df,instruments = get_binance_data()
# print(df)