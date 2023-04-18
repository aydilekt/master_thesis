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
trucks = trucks[(trucks.Origin_Country.isin(['DE']))]
trucks = trucks[(trucks.Destination_Country.isin(['FR']))]
for t in range(len(truck_list)):
    print(t)
    truck_sample = truck_list[t]
    rest_sample = rest_list[t]

    for i in range(0,5):
        type="-hs-filtered-S2.1-V06-"+str(i)+".xlsx"
        trucks_origin=trucks.loc[(trucks.Origin_X.between(Origin_X,Origin_X+4)) & (trucks.Origin_Y.between(Origin_Y,Origin_Y+3))]
        print(len(trucks_origin))
        truck_newdf = trucks_origin.loc[(trucks_origin.Destination_X.between(Destination_X+0.5,Destination_X+7)) & (trucks_origin.Destination_Y.between(Destination_Y-2,Destination_Y+3))]
        print(len(truck_newdf))
        truck = truck_newdf.sample(truck_sample)
        range_Origin= [truck['Origin_X'].min(),truck['Origin_Y'].min(),truck['Origin_X'].max(),truck['Origin_Y'].max()]
        range_Dest = [truck['Destination_X'].min(),truck['Destination_Y'].min(),truck['Destination_X'].max(),truck['Destination_Y'].max()]
        if rest_sample<=20:
            rest_origin = rest_places.loc[(rest_places.Longitude.between(range_Origin[0]-2,range_Origin[2])) & (rest_places.Latitude.between(range_Origin[1]-1,range_Origin[3]+2))]
            rest_newdf = rest_places.loc[(rest_places.Longitude.between(range_Dest[0]+2,range_Dest[2]+1)) & (rest_places.Latitude.between(range_Dest[1]+2,range_Dest[3]+2))]
            #rest_origin = rest_places.loc[(rest_places.Longitude.between(Origin_X-4, Origin_X+2.3)) & (rest_places.Latitude.between(Origin_Y-2, Origin_Y+2))]

        elif rest_sample==30:
            rest_origin = rest_places.loc[(rest_places.Longitude.between(range_Origin[0] - 2, range_Origin[2])) & (rest_places.Latitude.between(range_Origin[1] - 1.4, range_Origin[3]+2))]
            rest_newdf = rest_places.loc[(rest_places.Longitude.between(range_Dest[0] +2, range_Dest[2] + 1.5)) & (rest_places.Latitude.between(range_Dest[1] , range_Dest[3]+2))]

        else:
            rest_origin = rest_places.loc[(rest_places.Longitude.between(range_Origin[0] - 4, range_Origin[2])) & (
                rest_places.Latitude.between(range_Origin[1] - 2, range_Origin[3]+2))]
            rest_newdf = rest_places.loc[(rest_places.Longitude.between(range_Dest[0] + 2, range_Dest[2] + 2)) & (
                rest_places.Latitude.between(range_Dest[1]+2, range_Dest[3]+2))]

        print(len(rest_origin))
        #rest_newdf = rest_places.loc[(rest_places.Longitude.between(Destination_X-1,Destination_X+6)) & (rest_places.Latitude.between(Destination_Y,Destination_Y+4))]
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