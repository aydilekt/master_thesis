import random
import pandas as pd
import googlemaps
import haversine as hs
from math import radians, cos, sin, asin, sqrt

truck_list = [50,100,150,200,250,300]
rest_list = [10,20,30,40,50,60]
for t in truck_list:
    for r in rest_list:
        trucknum=t
        restplacenum=r
        for i in range(0,5):
            type="-hs-filtered-S2.2-V06-"+str(i)+".xlsx"
            trucks = pd.read_excel("sample_truck-"+str(trucknum)+str(type),sheet_name="truck")
            lat1_col = trucks.columns.get_loc('Origin_X')
            lon1_col = trucks.columns.get_loc('Origin_Y')
            destname_col=trucks.columns.get_loc('Destination_name')
            lat2_col = trucks.columns.get_loc('Destination_X')
            lon2_col = trucks.columns.get_loc('Destination_Y')
            dist_col =trucks.columns.get_loc('distances')

            trucks_list = trucks.values.tolist()

            rest_places = pd.read_excel("sample_restplaces-"+str(restplacenum)+str(type),sheet_name="restplaces")
            rest_columns = rest_places.columns
            title_col = rest_places.columns.get_loc('Title')
            rest_columns = rest_places.columns
            lat_rest_col= rest_places.columns.get_loc('Longitude')
            lon_rest_col=rest_places.columns.get_loc('Latitude')

            rest_places_list = rest_places.values.tolist()

            def haversine(lon1, lat1, lon2, lat2):
                lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
                return c * r

            def Origin_To_Hub():
                #time_list = []
                distance_list = []
                k=1
                for i in trucks_list:
                    print("1 -->"+str(k))
                    k = k + 1
                    temp_distance=[]
                    #temp_time=[]
                    LatOrigin = i[lat1_col]
                    LongOrigin = i[lon1_col]
                    for j in rest_places_list:
                        LatHub = j[lat_rest_col]
                        LongHub = j[lon_rest_col]
                        result1_distance = haversine(LongOrigin,LatOrigin,LongHub,LatHub)
                        temp_distance.append(result1_distance)
                    #time_list.extend([temp_time])
                    distance_list.extend([temp_distance])
                return distance_list

            def Hub_To_Hub():
                distance_list = []
                k=1
                for i in rest_places_list:
                    print("2 -->" + str(k))
                    k = k + 1
                    temp_distance = []
                    LatHub1 = i[lat_rest_col]
                    LongHub1 = i[lon_rest_col]
                    for j in rest_places_list:
                        if i!=j:
                            LatHub2 = j[lat_rest_col]
                            LongHub2 = j[lon_rest_col]
                            result1_distance = haversine(LongHub1, LatHub1,LongHub2, LatHub2)
                            temp_distance.append(result1_distance)
                        else:
                            temp_distance.append(0)
                    distance_list.extend([temp_distance])
                return distance_list

            def Hub_To_Destination():
                distance_list = []
                k=1
                for i in rest_places_list:
                    print("3 -->" + str(k))
                    k = k + 1
                    temp_distance = []
                    LatHub = i[lat_rest_col]
                    LongHub = i[lon_rest_col]
                    for j in trucks_list:
                        LatDes = j[lat2_col]
                        LongDes = j[lon2_col]
                        result1_distance = haversine(LongHub, LatHub, LongDes, LatDes)
                        temp_distance.append(result1_distance)
                    distance_list.extend([temp_distance])
                return distance_list

            if __name__ == "__main__":
                restplace_names = []
                for i in rest_places_list:
                    restplace_names.append(i[title_col])

                trucks_list = [i[0:dist_col+1] for i in trucks_list]
                distance_list = Origin_To_Hub()
                for i in range(len(trucks_list)):
                    for j in range(len(distance_list[0])):
                        trucks_list[i].append(distance_list[i][j])

                column_names = list(trucks.columns[0:dist_col+1]) + restplace_names
                df_OD = pd.DataFrame(trucks_list, columns=column_names)
                df_OD.to_excel("sample_modeldata_("+str(trucknum)+"-"+str(restplacenum)+")"+str(type), sheet_name="OriginToHub", index=False)

                print("Origin to Hub distances were calculated")
                df_HUB = pd.DataFrame(Hub_To_Hub(), columns=restplace_names)
                df_HUB.insert(0,column='',value=restplace_names)

                with pd.ExcelWriter("sample_modeldata_("+str(trucknum)+"-"+str(restplacenum)+")"+str(type), engine="openpyxl", mode='a') as writer:
                    df_HUB.to_excel(writer, sheet_name="HubToHub", index=False)

                print("Hub to Hub distances were calculated")

                destination_name=[]
                for i in trucks_list:
                    destination_name.append(i[destname_col])

                df_HD = pd.DataFrame(Hub_To_Destination(), columns=destination_name)
                df_HD.insert(0, column='', value=restplace_names)

                with pd.ExcelWriter("sample_modeldata_("+str(trucknum)+"-"+str(restplacenum)+")"+str(type), engine="openpyxl", mode='a') as writer:
                    df_HD.to_excel(writer, sheet_name="HubToDestination", index=False)

                print("Hub to Destination distances were calculated")
