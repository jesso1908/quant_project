import quantlib.data_utlis as du
import quantlib.general_utlis as gu
from dateutil.relativedelta import relativedelta
import pandas as pd
import json

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


from subsystems.LBMOM.subsys import Lbmom

# instruments,df = du.get_binance_data()
# df = du.extend_dataframe(instruments,df)

# gu.save_file("./price_data/data.obj_1",(df,instruments))


df, instruments = gu.load_file("./price_data/data.obj_1")
print(df)
# save instruments to json
# with open("./subsystems/LBMOM/config.json","w") as f:
# 	json.dump({"instruments":instruments},f,indent=4)


#run simulation for 5 years
VOL_TARGET = 0.20

sim_start = df.index[-1] - relativedelta(years=4)


strat = Lbmom(instruments_config="./subsystems/LBMOM/config.json", historical_df=df, simulation_start=sim_start, vol_target=VOL_TARGET)
strat.run_simulation()
# data = strat.extend_historicals()
# print(data)