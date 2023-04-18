import pandas as pd
from pandas import DataFrame
import json
import codecs
import googlemaps
import random

list_of_countries = ["DE", "FR", "IT", "CH", "ES", "BE", "NL","LU", "AT", "PT"]

restplaces_file = pd.read_csv("flixbus_service_stations_worldwide.csv")
restplaces_file = restplaces_file.rename(columns={'Stop name': 'Title'})
restplaces_file = restplaces_file[restplaces_file["Country code"].isin(list_of_countries)]
truck_new=pd.DataFrame()

def rest_places():
    df = pd.DataFrame(restplaces_file, columns=["Title","Latitude","Longitude","Country code"])
    df.to_excel("restplaces_data_europe.xlsx", index=False)
    print("restplaces_data_europe file is created")

if __name__ == "__main__":
    rest_places()
