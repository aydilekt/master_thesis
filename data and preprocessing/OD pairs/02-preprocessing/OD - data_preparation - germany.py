import pandas as pd
import json
import codecs
from math import radians, cos, sin, asin, sqrt

truckflow_df= pd.read_csv("01_Trucktrafficflow.csv")
regions_df=pd.read_excel("02_NUTS-3-Regions.xlsx")

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def truck_locations():
    merged_df1 = pd.merge(truckflow_df, regions_df, left_on='ID_origin_region', right_on='ETISPlus_Zone_ID')
    merged_df2 = pd.merge(truckflow_df, regions_df, left_on='ID_destination_region', right_on='ETISPlus_Zone_ID')
    truck_data = pd.merge(merged_df1, merged_df2, on=['ID_origin_region', 'Name_origin_region',
                                                      'ID_destination_region', 'Name_destination_region'])
    truck_data = truck_data.rename(columns={'Geometric_center_X_x': 'Origin_X', 'Geometric_center_Y_x': 'Origin_Y',
                                            'Geometric_center_X_y': 'Destination_X',
                                            'Geometric_center_Y_y': 'Destination_Y',
                                            'Country_x': 'Origin_Country', 'Country_y': 'Destination_Country'})
    truck_new = pd.DataFrame(truck_data,
                             columns=['ID_origin_region', 'Name_origin_region', 'Origin_Country', 'Origin_X',
                                      'Origin_Y',
                                      'ID_destination_region', 'Name_destination_region', 'Destination_Country',
                                      'Destination_X', 'Destination_Y'])
    mask = (truck_new['Origin_Country'] == 'DE') & (truck_new['Destination_Country'] == 'DE')
    truck_new = truck_new.loc[mask]
    truck_new = truck_new.drop('Origin_Country', axis=1)
    truck_new = truck_new.drop('Destination_Country', axis=1)
    truck_new.to_csv("truck_data.csv", index=False)
    print("truck_data file is created")

def calculate_distances():
    df = pd.read_csv("truck_data.csv")
    truck_list = df.values.tolist()
    distance_list = []

    for i in range(len(truck_list)):
        print(i)
        LatOrigin = truck_list[i][2]
        LongOrigin = truck_list[i][3]
        LatDestination = truck_list[i][6]
        LongDestination = truck_list[i][7]
        result = haversine(LongOrigin, LatOrigin,LongDestination, LatDestination)
        distance_list.append(result)
    df_distance = pd.DataFrame(distance_list, columns=["distances"])
    df['distances']=df_distance
    df.to_csv("truck_data.csv", index=False)

if __name__ == "__main__":
    #rest_places()
    truck_locations()
    calculate_distances()

