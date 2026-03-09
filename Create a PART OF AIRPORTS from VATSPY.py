### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###
### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###
### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###
### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###
### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###
### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS AFTERWARDS ###

airports_to_convert = """
EBAM|Amougies|50.739444|3.486111||EBBU|0
EBAR|Arlon/Sterpenich|49.662778|5.886944|QON|EBBU|0
EBAV|Hannut/Avernas-Le-Bauduin|50.706667|5.068056||EBBU|0
EBAW|Antwerpen|51.189444|4.460278||EBBU|0
EBBE|Beauvechain|50.757833|4.767||EBBU|0
EBBL|Kleine Brogel|51.168333|5.469722||EBBU|0
EBBN|Buellingen|50.415|6.276389||EBBU|0
EBBR|Bruxelles National|50.901389|4.484444||EBBU|0
EBBT|Brasschaat|51.33306|4.5||EBBU|0
EBBX|Bertrix Bel- AFB|49.89972|5.21639||EBBU|0
EBBY|Genappe/Baisy-Thy|50.568611|4.434722||EBBU|0
EBBZ|Pont-A-Celles/Buzet|50.541667|4.381111||EBBU|0
"""
lines = airports_to_convert.split("\n")
lines = [x for x in lines if x != '']

airports_dictionary = {}
for line in lines:
    line_parts = line.split("|")
    
    dict_contents = {}
    dict_contents["callsign"] = line_parts[1]
    dict_contents["coord"] =  [float(line_parts[2]),float(line_parts[3])]
    
    airports_dictionary[line_parts[0]] = dict_contents


final_dictionary = {
    "airports" : airports_dictionary
}

# Directly from dictionary
import json
with open('./Output/airports.json', 'w') as outfile:
    ### DO NOT FORGET TO ADD THE TOPDOWN KEY FOR RELEVANT AIRPORTS ###
    json.dump(final_dictionary, outfile)

print(final_dictionary)