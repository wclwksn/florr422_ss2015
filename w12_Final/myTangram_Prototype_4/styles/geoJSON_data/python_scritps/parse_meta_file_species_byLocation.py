import pandas as pd
import numpy as np
import json

csv = pd.read_csv('ALL_HIVE_DATA_preliminary_hive_analysis_colsFixed.csv')
samples = (u'Honey', u'Bee', u'Bee Debris Solid', u'Bee Debris Liquid',
       u'Propolis in Solvant', u'Ralph\'s Hand', u'Beeswax ',
       u'Outside Hive', u'Inside Hive', u'Scrapper', u'Propolis no solvent ')

taxonomy = {
    'k': 'kingdom',
    'p': 'phylum',
    'c': 'class',
    'o': 'order',
    'f': 'family',
    'g': 'genus',
    's': 'species',
    't': 'subspecies',
}

# 'ASTORIA HIVE',
#  'CROWN HEIGHTS - LANGSTROTH',
#  'CROWN HEIGHTS -TOP BAR',
#  'FORT GREENE'

# https://www.openstreetmap.org
#Astoria:
# max_lat = 40.7867
# min_lat = 40.7147
# max_lng = -73.8304
# min_lng = -73.9689

#Crown Heights:
# max_lat_ch = 40.7043
# min_lat_ch = 40.6287
# max_lng_ch = -73.8647
# min_lng = -74.0194

#Forte Greene:
# 40.7084
# 40.6706
# -73.9346
# -74.0119

#Note: you have to change these coordinates depenging on the location:
max_lat = 40.7084
min_lat = 40.6706
max_lng = -73.9346
min_lng = -74.0119
dlat = max_lat - min_lat
dlng = max_lng - min_lng


def generate_coordinates(amount):
    lat = np.random.uniform(min_lat, max_lat)
    lng = np.random.uniform(min_lng, max_lng)

    return [lng, lat]

features = []

def parse_row(row):
    hierarchy = row['ID'].split('|')

    if len(hierarchy) == 7:
        location = row['Location']
        if location != "FORT GREENE": #change the name 
            return

        # print "location_data:", location_data
        # if not output[location]:
            # only create empty samples if there is nothing in
            # output[location] already

        amount = np.max([row[sample] for sample in samples])


        species = hierarchy[-1].split('__')[1]
        
        #using the ceiling to draw the points
        #if you 100% abundance == 100 points
        number_of_points = int(np.ceil(amount))
        for i in xrange(number_of_points):
            geometry = {
                'type': 'Point',
                'coordinates': generate_coordinates(amount)
            }
            data = {
                'location': location,
                'species': species,
                'percentage': amount,
                'kind': 'bacteria',
            }
            feature = {
                'geometry': geometry,
                'type': "Feature",
                'properties': data,
            }

            features.append(feature)


csv.apply(parse_row, axis=1) 

output = {
    'type': "FeatureCollection",
    'features': features,
}
#chane the name of the output file:
json.dump(output, open('meta_file_species_Point_FortGreen.json', 'w'), indent=2, separators=(',', ': '))

