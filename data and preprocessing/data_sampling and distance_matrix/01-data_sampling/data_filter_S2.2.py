import random
import pandas as pd
from math import radians, cos, sin, asin, sqrt


trucks = pd.read_csv("truck_data_europe.csv")
rest_places = pd.read_excel("restplaces_data_europe.xlsx")


truck_list = [50,100,150,200,250,300]
rest_list = [10,20,30,40,50,60]
Origin_X = 11.8
Origin_Y =51.6
Destination_X = -1
Destination_Y = 42.8
trucks=trucks.loc[(trucks.distances>1000)]

for t in range(len(truck_list)):
    truck_sample = truck_list[t]
    rest_sample = rest_list[t]
    for i in range(0,5):
        type="-hs-filtered-S2.2-V06-"+str(i)+".xlsx"
        trucks_origin=trucks.loc[(trucks.Origin_X.between(Origin_X-1,Origin_X+5)) & (trucks.Origin_Y.between(Origin_Y-7,Origin_Y+2))]
        print(len(trucks_origin))
        truck_newdf = trucks_origin.loc[(trucks_origin.Destination_X.between(Destination_X-2,Destination_X+3)) & (trucks_origin.Destination_Y.between(Destination_Y-3,Destination_Y+4))]
        print(len(truck_newdf))
        grouped = truck_newdf.groupby(['Origin_X', 'Origin_Y', 'Destination_X', 'Destination_Y']).agg('size')
        origins = grouped.reset_index()[['Origin_X', 'Origin_Y']].drop_duplicates()
        destinations = grouped.reset_index()[['Destination_X', 'Destination_Y']].drop_duplicates()
        filtered_df = truck_newdf[
            (truck_newdf['Origin_X'].isin(origins['Origin_X'])) & (truck_newdf['Origin_Y'].isin(origins['Origin_Y'])) &
            (truck_newdf['Destination_X'].isin(destinations['Destination_X'])) & (
                truck_newdf['Destination_Y'].isin(destinations['Destination_Y']))]
        truck = filtered_df.sample(truck_sample)
        rest_origin = rest_places.loc[(rest_places.Longitude.between(Origin_X-3, Origin_X+2)) & (rest_places.Latitude.between(Origin_Y-6, Origin_Y+1))]
        print(len(rest_origin))
        rest_newdf = rest_places.loc[(rest_places.Longitude.between(Destination_X-3,Destination_X+6)) & (rest_places.Latitude.between(Destination_Y,Destination_Y+4))]
        print(len(rest_newdf))
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