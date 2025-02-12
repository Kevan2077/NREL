import os

import numpy as np
import pandas as pd



path=f"D:\\Do it\\Phd\\Pycharm project\\NREL\\DATA\\SAM_INPUTS\\WEATHER_DATA"
for i in range(3,340):
    file_path=path+os.sep+f"weather_data_Point {i}_2023.csv"
    data=pd.read_csv(file_path, index_col=0)
    data = data.set_index(data.columns[0])

    #data = data.drop(data.columns[0], axis=1)
    data.to_csv(file_path)