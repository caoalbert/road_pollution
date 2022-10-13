from datetime import datetime
import clean_pollution
import pandas as pd
import datetime

def clean_traffic():
    flow = pd.read_excel("交通流参数.xlsx").iloc[:,7:]
    flow = flow.dropna(how = "all")

    output = pd.DataFrame(columns = ["average_delay", "stops", "stop_delay", "average_speed", "date", "time"])
    hour = [i*0.5 for i in range(12, 49)]
    date = datetime.date(2022, 6, 12)

    for i in range(flow.shape[0]):
        if i in [i*5 for i in range(10)]: 
            pass
        elif i in [i*5+1 for i in range(10)]:
            average_delay = flow.iloc[i,:].transpose().reset_index(drop = True)
        elif i in [i*5+2 for i in range(10)]:
            stops = flow.iloc[i,:].transpose().reset_index(drop = True)
        elif i in [i*5+3 for i in range(10)]:
            stop_delay = flow.iloc[i,:].transpose().reset_index(drop = True)
        elif i in [i*5+4 for i in range(10)]:
            average_speed = flow.iloc[i,:].transpose().reset_index(drop = True)
            date_series = pd.Series(date).repeat(len(hour)).reset_index(drop = True)
            hour_series = pd.Series(hour).reset_index(drop = True)
            to_join = pd.concat([average_delay, stops, stop_delay, 
                                average_speed, date_series,
                                hour_series], axis = 1)
            to_join.drop(to_join.tail(1).index, inplace = True)
            to_join.columns = ["average_delay", "stops", "stop_delay", "average_speed", "date", "time"]
            output = pd.concat([output, to_join], axis  = 0)
            date += datetime.timedelta(days = 1)
            
    output["Hour"] = output["time"] // 1
    output["Minute"] = output["time"] % 1 * 60
    output["Hour"] = output["Hour"].astype("int")
    output["Minute"] = output["Minute"].astype("int")
    output["date"] = pd.to_datetime(output["date"])
    output["Month"] = output["date"].dt.month
    output["Day"] = output["date"].dt.day
    output.drop(["time", "date"], 1, inplace = True)
            
    return(output)
        