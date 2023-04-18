import pandas as pd
from pandas import DataFrame
import json
import codecs
import googlemaps
import random

autobahn_file = pd.read_excel("Autobahn_info.xlsx")
autobahn_list = autobahn_file.values.tolist()
def rest_places():
    files=[]
    for i in range(len(autobahn_file)):
        files.append(codecs.open(autobahn_list[i][5],"r","utf-8"))

    restarea_list = []
    k=0 #start file

    for j in files:
        data = json.load(j) #load each json file (A1,A2,...,A99) seperately
        data_length = len(data['parking_lorry'])
        description = []

        for i in range(data_length):
            roadId =data['parking_lorry'][i]['title'][0:4].replace(" ","")
            title=data['parking_lorry'][i]['subtitle'][1:-1]
            lat = data['parking_lorry'][i]['coordinate']['lat']
            long = data['parking_lorry'][i]['coordinate']['long']
            description = data['parking_lorry'][i]['description']
            if len(description)==1:
                size=data['parking_lorry'][i]['description'][0]
            elif len(description)==0:
                size= "NA"
            else:
                string = data['parking_lorry'][i]['description'][1]
            removed = (string[:-1])
            size = int(removed[len(string) - 3:])
            restarea_list.append([roadId,title,lat,long,size])
        j.close()

    df = pd.DataFrame(restarea_list, columns=["RoadID","Title","Latitude","Longitude","# of Park Places(trucks)"])
    df.to_excel("restplaces_data.xlsx", index=False)

if __name__ == "__main__":
    rest_places()
