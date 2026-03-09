""""
This file may be used to update your positions key when new sectors are added, or frequencies are changed.
It returns the position key with the previously issued colors, unless it is a new sector.


Create a new file in the Input folder called 'Positions_VG.json'. 
This file should be a json of the VG-key "Positions". I included an example of its contents. You should copy it from the VG repo (not beta)

A new file will be created './Output/positions_update.json'. Additionally, for your convenience, each position will be printed with its corresonding color,
as well as if a new color was assigned.

"""



import json
with open('VATGlasses Data/VC-VR.txt') as f:
    sectors = f.readlines()
with open('VATGlasses Data/vc-vr.json') as f:
    colors = json.load(f)["positions"]


# Attempt to create random colors for every position, but in a way that also attempts to keep similar tints for similar positions types
def similarhex(pos, colors):
    
    if pos in colors:
        print(pos, colors[pos]["colours"][0]["hex"])

        return colors[pos]["colours"][0]["hex"]
    else:
        print("Random color for", pos, "- New entry or no last assigned color")
        import random
        color = tuple(random.choices(range(256), k=3))
        r, g, b = color
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Removes comments from file
def cleanup(file):
    textfile = ""

    for line in file:
        line = line.split(';')[0]
        if line != "":
            textfile += line
    
    for i in range(5): # random number lol
        textfile = textfile.replace("\n\n", "\n")
    
    return textfile

sectors = cleanup(sectors)

sectors = sectors.split("\n")


positions = [i for i in sectors if i]  # only keeping the items (sectors) that are truthy, that is, not empty strings or None values

id_dict = {}
for pos in positions:
    parts = pos.split(":")
    id = parts[3]
    tmp = {
        "callsign" : parts[1],
        "frequency" : parts[2],
        "type" : parts[6],
        "pre" : [parts[5]]
        #tmp["colours"] = [{"hex": similarhex(id,colors)}] --- added later to make it more visible which sectors are added
    }



    # Allow these position types for the new file
    if tmp["type"] != "ATIS"  and tmp["type"] != "GND" and tmp["type"] != "DEL":
        tmp["colours"] = [{"hex": similarhex(id,colors)}]
        id_dict[id] = tmp 


pos_dict =  {}
pos_dict["positions"] = id_dict

print(pos_dict)

# Directly from dictionary
with open('VATGlasses Data/vc-vr.json', 'w') as outfile:
    json.dump(pos_dict, outfile)