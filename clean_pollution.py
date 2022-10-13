import os
from time import strptime
import pandas as pd


def clean_pollution():

    subfolders = os.listdir("pollution_data/")

    for i in subfolders:
        if i[0] != "6":
            subfolders.remove(i)

    pollution = pd.DataFrame()

    for j in subfolders:
        subfolder_path = "pollution_data/" + j
        csv = os.listdir(subfolder_path)
        for k in csv:
            path = "pollution_data/" + str(j) + "/" + str(k)
            df = pd.read_csv(path, skiprows = 32, names = ["Date", "Time", "pm25"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Time"] = pd.to_datetime(df["Time"])
            df["Day"] = df["Date"].dt.day.astype("int")
            df["Month"] = df["Date"].dt.month.astype("int")
            df["Hour"] = df["Time"].dt.hour.astype("int")
            df["Minute"] = df["Time"].dt.minute.astype("int")
            df["Second"] = df["Time"].dt.second.astype("int")
            df = df[["Month", "Day", "Hour", "Minute", "Second", "pm25"]]
            df["Period"] = k[4]
            df["Mode"] = str.split(str.split(k)[1], ".")[0]
            pollution = pollution.append(df)
        
    pollution.loc[pollution["Mode"] == 'bus（7', "Mode"] = "bus"
    return(pollution)
            
        
        
        

