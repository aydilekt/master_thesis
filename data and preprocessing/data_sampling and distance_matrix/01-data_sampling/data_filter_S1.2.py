import random
import pandas as pd
from math import radians, cos, sin, asin, sqrt


trucks = pd.read_csv("truck_data.csv")

truck_list = [300]
rest_list = [60]
Origin_X=6.8
Origin_Y=47.6
Destination_X=11.8
Destination_Y=51.5

for t in range(1):
    truck_sample = truck_list[t]
    rest_sample = rest_list[t]
    for i in range(0,3):
        type="-hs-filtered-S1.2-"+str(i)+".xlsx"
        trucks_origin=trucks.loc[(trucks.Origin_X.between(Origin_X-1,Origin_X+3)) & (trucks.Origin_Y.between(Origin_Y-1,Origin_Y+6))]
        print(len(trucks_origin))
        truck_newdf = trucks_origin.loc[(trucks_origin.Destination_X.between(Destination_X-1,Destination_X+2)) & (trucks_origin.Destination_Y.between(Destination_Y-2,Destination_Y+5))]
        print(len(truck_newdf))
        truck = truck_newdf.sample(truck_sample)
        range_Origin= [truck['Origin_X'].min(),truck['Origin_Y'].min(),truck['Origin_X'].max(),truck['Origin_Y'].max()]
        range_Dest = [truck['Destination_X'].min(),truck['Destination_Y'].min(),truck['Destination_X'].max(),truck['Destination_Y'].max()]
        rest_places = pd.read_excel("restplaces_data.xlsx")
        rest_origin = rest_places.loc[(rest_places.Longitude.between(range_Origin[0]+1.5,range_Origin[2]+0.5)) & (rest_places.Latitude.between(range_Origin[1]+1,range_Origin[3]))]
        rest_newdf = rest_places.loc[(rest_places.Longitude.between(range_Dest[0]-2,range_Dest[2]-1)) & (rest_places.Latitude.between(range_Dest[1]+0.5,range_Dest[3]-0.5))]

        rest1 = rest_origin.sample(int(rest_sample/2))
        rest2= rest_newdf.sample(int(rest_sample/2))
        data_frame=[rest1,rest2]
        rest_new=pd.concat(data_frame)
        list_truck=[Origin_X,Origin_Y,Destination_X,Destination_Y]
        list_rest=[Origin_X,Origin_Y,Destination_X,Destination_Y]

        data_frame02 = pd.DataFrame(list_truck)
        data_frame02.to_excel("sample_truck-"+str(truck_sample)+str(type), sheet_name="Info", index=False)

        with pd.ExcelWriter("sample_truck-"+str(truck_sample)+str(type), engine="openpyxl", mode='a') as writer:
            truck.to_excel(writer, sheet_name="truck", index=False)

        data_frame02 = pd.DataFrame(list_rest)
        data_frame02.to_excel("sample_restplaces-"+str(rest_sample)+str(type), sheet_name="Info", index=False)

        with pd.ExcelWriter("sample_restplaces-"+str(rest_sample)+str(type), engine="openpyxl", mode='a') as writer:
            rest_new.to_excel(writer, sheet_name="restplaces", index=False)