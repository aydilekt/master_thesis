import pandas as pd
from math import radians, cos, sin, asin, sqrt


list_of_countries = ["DE", "FR", "IT", "CH", "ES", "BE", "NL","LU", "AT", "PT"]

truckflow_df= pd.read_csv("01_Trucktrafficflow.csv") #takes too long to read because of the size
regions_df=pd.read_excel("02_NUTS-3-Regions.xlsx")
regions_df = pd.DataFrame(regions_df, columns=["ETISPlus_Zone_ID","Country","Geometric_center_X","Geometric_center_Y"])
regions_df = regions_df[regions_df.Country .isin(list_of_countries)]



def get_truck_locations():
    # merge the two data sets based IDs to get the coordinates
    merged_df1 = pd.merge(truckflow_df, regions_df, left_on='ID_origin_region', right_on='ETISPlus_Zone_ID')
    merged_df2 = pd.merge(truckflow_df, regions_df, left_on='ID_destination_region', right_on='ETISPlus_Zone_ID')
    truck_data = pd.merge(merged_df1, merged_df2,on=['ID_origin_region', 'Name_origin_region',
                             'ID_destination_region','Name_destination_region' ])
    truck_data = truck_data.rename(columns={'Geometric_center_X_x': 'Origin_X','Geometric_center_Y_x': 'Origin_Y',
                            'Geometric_center_X_y': 'Destination_X','Geometric_center_Y_y': 'Destination_Y',
                            'Country_x':'Origin_Country','Country_y':'Destination_Country'})
    truck_new=pd.DataFrame(truck_data, columns= ['ID_origin_region', 'Name_origin_region','Origin_Country','Origin_X','Origin_Y',
                             'ID_destination_region','Name_destination_region', 'Destination_Country','Destination_X','Destination_Y'])
    truck_new.to_csv("truck_data_europe.csv", index=False)
    print("truck_data_europe file is created")

def rest_places():
    df = pd.DataFrame(autobahn_file, columns=["Title","Latitude","Longitude","Country code"])
    df.to_excel("restplaces_data_europe.xlsx", index=False)
    print("restplaces_data_europe file is created")


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


def calculate_distances():
    df = pd.read_csv("truck_data_europe.csv")
    truck_list = df.values.tolist()
    distance_list = []

    for i in range(len(truck_list)):
        print(i)
        LatOrigin = truck_list[i][4]
        LongOrigin= truck_list[i][3]
        origin = (LatOrigin, LongOrigin)
        LatDestination = truck_list[i][9]
        LongDestination = truck_list[i][8]
        destination = (LatDestination, LongDestination)
        result = haversine(LongOrigin, LatOrigin,LongDestination, LatDestination)
        distance_list.append(result)
    df_distance = pd.DataFrame(distance_list, columns=["distances"])
    df_distance.to_csv("truck_data_europe.csv", index=False)
    print("distances between Origin and Destinations are calculated. truck_data_europe_distances file is created")

if __name__ == "__main__":
    rest_places()
    get_truck_locations()
    calculate_distances()


