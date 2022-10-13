# Import cleaning functions
import clean_pollution
import clean_traffic
import clean_gps
from importlib import reload
reload(clean_gps)

# Load the data
pollution = clean_pollution.clean_pollution()
traffic = clean_traffic.clean_traffic()
gps = clean_gps.clean_gps()
        
# Merge pollution and gps
merged = pollution.merge(gps, on = ["Month", "Day", "Hour", "Minute", "Second", "Mode"], how = "left", copy = False)

# Check missing gps data
missing_coord = merged["LATITUDE N/S"].isna().sum()
print("There are", missing_coord, "out of", merged.shape[0], "observations that don't have gps data")

# Merge with traffic
merged["minute_merging_traffic"] = 30
merged.loc[(merged["Minute"] >= 45) & (merged["Minute"] < 15), "minute_merging_traffic"] = 0
traffic["minute_merging_traffic"] = traffic["Minute"]

merged_traffic = merged.merge(traffic, on = ["Hour", "Day", "minute_merging_traffic", "Month"], how = "left", copy = False)
merged_traffic.drop(["Minute_y", "minute_merging_traffic"], 1, inplace = True)

merged_traffic.to_csv("merged_data.csv", index = False)


