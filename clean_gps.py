import pandas as pd
import os

def clean_gps():
    subfolders = os.listdir("gps/")

    output = pd.DataFrame()
    for i in subfolders:
        path = "gps/" + i
        sub_subfolders = os.listdir(path)
        for j in sub_subfolders:
            path2 = path + "/" + j
            month = j[0:1]
            day = j[2:4]
            Mode = j.split()[1]
            
            df = pd.read_csv(path2)
            df = df[["TIME", 'LATITUDE N/S' , 'LONGITUDE E/W', "HEADING"]]
            
            df.loc[df["TIME"] <= 210000, "TIME"] = df["TIME"] + 80000
            df.loc[df["TIME"] > 220000, "TIME"] = df["TIME"] - 160000
            
            df["Month"] = month
            df["Day"] = day
            df["Mode"] = Mode
            df["TIME"] = df["TIME"].astype("str")
            df["Second"] = df["TIME"].str[-2:]
            df["Minute"] = df["TIME"].str[-4:-2]
            df["Hour"] = df["TIME"].str[-6:-4]

            df["Month"] = df["Month"].astype("int")
            df["Day"] = df["Day"].astype("int")
            df["Second"] = df["Second"].astype("int")
            df["Minute"] = df["Minute"].astype("int")
            df["Hour"] = df["Hour"].astype("int")
            df.drop("TIME", 1, inplace = True)
            
            output = pd.concat([output, df], 0)
            
    return output