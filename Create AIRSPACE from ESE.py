import json
import re

FIR_ids_for_this_vacc = ["VCCF","VRMF"]


# A file containing only SECTOR data, limited noise (white lines, comments) is allowed. 
with open('VATGlasses Data/AIRSPACE.txt',"r",encoding='utf-8') as f:
    # File like:
    # SECTOR:EBBU·EBBE TMA1A·025·035:02500:03500
    # OWNER:MIL:BI
    # BORDER:114:115:116:117:118:119:120:121:122:123:124:125

    sectors = f.readlines() 

# Converts more than two white spaces into exactly two white spaces (necessary for splitting)
def filter_string(string):
    return re.sub(r'(\n){3,}', r'\n\n', string)

# Removes comments from file
def cleanup(file):
    textfile = ""

    for line in file:
        line = line.split(';')[0]

        if line != "":
            textfile += line.strip() + "\n"
    
    return filter_string(textfile.replace("�","·").replace("�","·"))

sectors = cleanup(sectors)
sectors = sectors.split("\n\n")


sectors = [i for i in sectors if i] # only keeping the items (sectors) that are truthy, that is, not empty strings or None values

sectordic = {}

# Removes string OWNER from the line and returns all sector owners' names/ids
def splitowners(line):
    #print(line)
    line = [x for x in line if x.startswith("OWNER:")]
    try:
        return line[0].split(":")[1:]
    except:
        # If this also fails: enable print and search for the owner name in the ese. Check if the line/list above/under is not empty/exists. This might be because the current line does not have a OWNER attirbute in the ESE.  - Check the ese!
        return line[0]

# Removes string BORDER from the line and returns all borderlines' names/numbers
def splitborders(line):
    #print(line)
    line = [x for x in line if x.startswith("BORDER:")]
    try:
        return line[0].split(":")[1:]
    except:
        # If this also fails: enable print and search for the border name in the ese. Check if the line/list above/under is not empty/exists. This might be because the current line does not have a BORDER attirbute in the ESE.  - Check the ese!
        return line[0]
    
# Dictionary with information about the sectors (no coordinates yet, only border names/numbers)
for sector in sectors:
    line = sector.split("\n")
    name = line[0].split(":")[1]
    low = line[0].split(":")[22]
    high = line[0].split(":")[3]
    owners = splitowners(line)
    borders = splitborders(line)
    
    sectordic[name] = {
        "low": low,
        "high" : high,
        "owners" : owners,
        "borders": borders,
    }

# A file containing only SECTORLINES, limited noise (white lines, comments) is allowed. 
with open('VATGlasses Data/AIRSPACE.txt') as f:
    # File like:
    # SECTORLINE:572
    # COORD:502517:0004917
    # COORD:502405:0004611

    textfile = f.readlines()

sectorlines = cleanup(textfile)
sectorlines = sectorlines.split("\n\n")

# Formats all coordinates of a given sectorline
def getcoor(line):
    coorlines = [x for x in line if x.startswith("COORD:")]
    coors = []
    for coorline in coorlines:
        coorline = coorline.replace("COORD:", "")
        coorline = [coorline.split(":")[0],coorline.split(":")[1]]
        coors.append(coorline)
    return coors
        

# Dictionary of linedic<sectorline_name> = {coor : [[bla,blabla][bla,bla,bla]]}
linedic = {}
for sectorline in sectorlines:
    if sectorline.startswith("\n"):
        sectorline = sectorline[2:]

    lines = sectorline.split("\n")
    coor = getcoor(lines)
    
    name = lines[0].split(":")[1]
    
    linedic[name] = {
        "coor" : coor
    }
        
# Connects all sector lines into one big line
def chain(dominoes):
    #print("\n",dominoes)
    #print("Before", linedic["176"])
    for i in range(len(dominoes) - 1):
        for j in range(len(dominoes) - 1):
            j += i + 1

            if dominoes[i][-1] == dominoes[j][0]: # head == tail
                #print("head=tail",dominoes[i],dominoes[j])
                rev = dominoes[j]
                new_list = dominoes[i] + rev
                dominoes[i] = new_list
                #dominoes[i].extend(rev)
                dominoes.remove(dominoes[j])
            
                if len(dominoes) == 1:
                    return dominoes[0]
                else:
                    return chain(dominoes)

            elif dominoes[i][-1] == dominoes[j][-1]: # head == head
                #print("head=head",dominoes[i][-1],dominoes[i],dominoes[j])
                rev = dominoes[j][::-1]
                new_list = dominoes[i] + rev
                dominoes[i] = new_list
                #dominoes[i].extend(rev)
                dominoes.remove(dominoes[j])
                
                if len(dominoes) == 1:
                    return dominoes[0]
                else:
                    return chain(dominoes)

            elif dominoes[i][0] == dominoes[j][0]: # tail == tail
                #print("tail=tail",dominoes[i][0],dominoes[i],dominoes[j])
                dominoes[i] = dominoes[j][::-1] + dominoes[i]
                dominoes.remove(dominoes[j])
                
                if len(dominoes) == 1:
                    return dominoes[0]
                else:
                    return chain(dominoes)

            elif dominoes[i][0] == dominoes[j][-1]: # tail == head
                #print("tail=head",dominoes[i][0],dominoes[i],dominoes[j])
                dominoes[i] = dominoes[j] + dominoes[i]
                dominoes.remove(dominoes[j])
                
                if len(dominoes) == 1:
                    return dominoes[0]
                else:
                    return chain(dominoes)

def removesequentialduplicates(coors):
    new_coors = []
    prev = ""
    
    for coor in coors:
        if coor != prev:
            new_coors.append(coor)
        prev = coor
    
    return new_coors

#Creates a nested list of the secotors' coordinates
def getpoints(borders):
    coordinates = []
    for b in borders:
        coordinates.append(linedic[b]["coor"])

    if len(coordinates) == 1:
        return coordinates[0]
    else:    
        coordinates_copy = coordinates.copy()
        return removesequentialduplicates(chain(coordinates_copy))


WordOfGodFinalDict = {}
airspaces = []

# Used to assign the sector a group based on the sectors' name
def findname(sector):
    vacc = sector.split("·")[0]
    group = sector.split("·")[1]

    if group.startswith("LSASZ"):
        return "LSAZ"

    # elif group.startswith("LSASG"):
    #     return "LSAG"
    
    # elif group.startswith("LSAS"):
    #     return "LSAS"
    
    # elif group.startswith("CBWV"):
    #     return "CBWV"

    # elif group.startswith("ZEELAND"):
    #     return "ZEELAND"  

    # elif vacc.startswith("ACI"):  
    #     return "ACI"

    # elif group.endswith("AREA"):  
    #     return "AREA"
    
    ## Do NOT REMOVE, this is your fail safe - Do **not** add this key to your groups json
    else:
        return "OTHER"

# Creates the output and is the heart of the code
for sector in reversed(sectordic.keys()):
    try:
        print(sector)
        name = sector.split("·")[1]
        
        if sector.split("·")[0] in FIR_ids_for_this_vacc: #If this sector is a sector of the vacc
            tmp = {}
            tmp["id"] = name
            tmp["group"] = findname(sector)
            tmp["owner"] = sectordic[sector]["owners"]
            tmp["sectors"] = [ {
                "min" : int(int(sectordic[sector]["low"])/100) ,
                "max": int(int(sectordic[sector]["high"])/100) -1,
                "points" : getpoints(sectordic[sector]["borders"])
            }]

            if tmp["sectors"][0]["points"] != None and not name.endswith("GND") and not name.endswith("DEL"): #and "-GND" not in name
                        airspaces.append(tmp)

        else:
            print("         not part of this vacc", FIR_ids_for_this_vacc)

    except:
        print("FAILED", sector)
        continue

WordOfGodFinalDict["airspace"] = airspaces

# Directly from dictionary
with open('VATGlasses Data/data/vc-vr.json', 'w') as outfile:
    json.dump(WordOfGodFinalDict, outfile)
