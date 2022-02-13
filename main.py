# import data as du
# import general_utlis as gu 

# df,instruments = du.get_binance_data()
# df_1 = du.extend_dataframe(traded=instruments,df=df)
# gu.save_file("./price_data/data.obj",(df_1,instruments))

import pandas as pd 
df = pd.read_csv('price_data/stock_data_2.csv',index_col='date')
df.index = pd.to_datetime(df.index)
print(df)