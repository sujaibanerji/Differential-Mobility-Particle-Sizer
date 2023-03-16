from datetime import date, timedelta
import os
import pandas as pd
from cmcrameri import cm
import matplotlib.pyplot as plt

level_zero_path = r'C:\LocalData\sujaiban\sujai.banerji\Aerosol Optical Properties\dmps'
start_date = 20200101
end_date_plus_one = 20220101

y1 = int(str(start_date)[0:4])
m1 = int(str(start_date)[4:6])
d1 = int(str(start_date)[6:8])

y2 = int(str(end_date_plus_one)[0:4])
m2 = int(str(end_date_plus_one)[4:6])
d2 = int(str(end_date_plus_one)[6:8])

start_datetime = date(y1, m1, d1)
end_datetime_plus_one = date(y2, m2, d2)  
    
def daterange(start_datetime, end_datetime_plus_one):
    for n in range(int((end_datetime_plus_one - start_datetime).days)):
        yield start_datetime + timedelta(n)
    
start_datetime_plus_one = start_datetime + timedelta(1)
start_datetime_file_name = 'dm' + str(start_datetime.strftime('%Y%m%d'))[2:8] + '.txt'
level_one_name = str(start_datetime_plus_one.year)
level_one_path = os.path.join(level_zero_path, level_one_name)
start_datetime_file_path = os.path.join(level_one_path, start_datetime_file_name)
df_start = pd.read_csv(start_datetime_file_path, sep = '\s+')
dmps_diameters = []
dmps_diameters = df_start.columns.values[2:40]    
df_dmps_diameters = pd.DataFrame(dmps_diameters)
df_start_values = df_start.iloc[:, 2:40]
df_start_values = df_start_values.reset_index()
df_start_values = df_start_values.iloc[:, 1:39]
df_start_timestamps = df_start.iloc[:, 0] 
df_start_timestamps = df_start_timestamps.to_frame()
df_start_timestamps.iloc[:, 0] = df_start_timestamps.iloc[:, 0].astype(float)
df_start_timestamps.iloc[:, 0] = df_start_timestamps.iloc[:, 0].astype(str).str[:6].astype(float)
df_start_timestamps.iloc[:, 0] = df_start_timestamps.iloc[:, 0] - float(start_datetime.day)
df_start_timestamps.iloc[:, 0] = df_start_timestamps.iloc[:, 0].astype(str).str[:6].astype(float)
df_start_values_frames = []
df_start_values_frames = [df_start_timestamps, df_start_values]
df_start_values = pd.concat(df_start_values_frames, axis = 1)
df_start_values_frames = []
df_start_values_np = df_start_values.to_numpy()
df_start_values = pd.DataFrame(df_start_values_np)
    
n = 1

for single_date in daterange(start_datetime_plus_one, end_datetime_plus_one):
    level_one_name = str(single_date.year)
    level_one_path = os.path.join(level_zero_path, level_one_name)
    level_two_name = 'dm' + str(single_date.strftime('%Y%m%d'))[2:8] + '.txt'
    level_two_path = os.path.join(level_one_path, level_two_name)
    if os.path.exists(level_two_path) == True:
        df_rest = pd.read_csv(level_two_path, sep = '\s+')
        df_rest_values = df_rest.iloc[:, 2:40]
        df_rest_values = df_rest_values.reset_index()
        df_rest_values = df_rest_values.iloc[:, 1:39]
        df_rest_timestamps = df_rest.iloc[:, 0] 
        df_rest_timestamps = df_rest_timestamps.to_frame()
        df_rest_timestamps = df_rest_timestamps - df_rest_timestamps.astype(int)
        if (df_rest_timestamps.iloc[0, 0] < 0.006944):
            df_rest_timestamps.iloc[0, 0] = 0
        df_rest_timestamps = df_rest_timestamps.transpose()
        df_rest_timestamps = df_rest_timestamps.reset_index()
        df_rest_timestamps = df_rest_timestamps.iloc[0, 1:]
        df_rest_timestamps = df_rest_timestamps.to_frame()
        df_rest_values_frames = [df_rest_timestamps, df_rest_values]
        df_rest_values = pd.concat([df_rest_timestamps, df_rest_values], axis = 1)     
        df_rest_values_np = df_rest_values.to_numpy()
        df_rest_values = pd.DataFrame(df_rest_values_np)
        n = n + 1
        common_timestamps = abs(df_start_values.iloc[:, 0] - df_rest_values.iloc[:, 0]) <= 0.006944
        df_rest_values.loc[common_timestamps, 1:40] = df_start_values.loc[common_timestamps, 1:40] + df_rest_values.loc[common_timestamps, 1:40]

df_rest_values.iloc[:, 1:39] = df_rest_values.iloc[:, 1:39]/n
df_rest_values = df_rest_values.transpose()
df_rest_values.columns = df_rest_values.iloc[0, :].astype(str).str[:8].astype(float)
df_rest_values = df_rest_values.iloc[1:, :]
df_rest_values = df_rest_values.reset_index()
df_rest_values = df_rest_values.iloc[:, 1:]
df_rest_values = pd.concat([df_dmps_diameters, df_rest_values], axis = 1)
df_rest_values = df_rest_values.set_index(df_rest_values.iloc[:, 0])
df_rest_values = df_rest_values.iloc[:, 1:].astype(float)

plt.imshow(df_rest_values, interpolation = 'none', cmap = cm.batlow, origin = 'lower')  
plt.colorbar()