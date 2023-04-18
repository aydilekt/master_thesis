import random
import pandas as pd
from math import radians, cos, sin, asin, sqrt

trucks = pd.read_csv("truck_data_europe.csv")
rest_places = pd.read_excel("restplaces_data_europe.xlsx")
trucks = trucks[trucks.distances > 600]

truck_list = [50,100,150,200,250,300]
rest_list = [10,20,30,40,50,60]

for t in range(len(truck_list)):
    truck_sample = truck_list[t]
    rest_sample = rest_list[t]
    for i in range(0,5):
        print(i)
        type = "-hs-random-S2.3-"+str(i)+".xlsx"
        truck_sampled = trucks.sample(truck_sample)
        rest_sampled = rest_places.sample(rest_sample)
        truck_sampled.to_excel("sample_truck-"+str(truck_sample)+str(type), sheet_name="truck", index=False)
        rest_sampled.to_excel("sample_restplaces-"+str(rest_sample)+str(type), sheet_name="restplaces", index=False)

