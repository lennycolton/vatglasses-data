import json


# File like

# ; ACC ------------------------------------
# Brussels West/Combined Control:Brussels Control:131.100:BW:W:EBBU:CTR:-:-:7101:7177
# Brussels East Control:Brussels Control:129.575:BE:E:EBBU:CTR:-:-:7101:7177

# Brussels NLS Control:Brussels Control:128.800:BN:N:EBBU:CTR:-:-:7101:7177
# Brussels HUS Control:Brussels Control:128.200:BH:H:EBBU:CTR:-:-:7101:7177
# Brussels LUS Control:Brussels Control:125.000:BL:L:EBBU:CTR:-:-:7101:7177
# Brussels WHS Control:Brussels Control:127.225:BC:C:EBBU:CTR:-:-:7101:7177

# Brussels Supervisor:Brussels Supervisor:199.998:BSUP:S:EBBU:CTR:-:-:7101:7177
# Brussels Information:Brussels Information:126.900:BI:I:EBBU:CTR:-:-:0040:0047

# ; UAC ------------------------------------
# Brussels Upper Control:Maastricht Radar:126.000:BU:U:EBBU:CTR:-:-:7101:7177

# Maastricht NIK:Maastricht Radar:135.975:YN:N:EDYY:CTR:-:-:7101:7177
# Maastricht LNO:Maastricht Radar:132.850:YO:O:EDYY:CTR:-:-:7101:7177
# Maastricht KOK:Maastricht Radar:132.200:YK:K:EDYY:CTR:-:-:7101:7177
# Maastricht LUX:Maastricht Radar:133.350:YL:L:EDYY:CTR:-:-:7101:7177

# ;Maastricht NIK HIGH:Maastricht Radar:132.750:YNH:A:EDYY:CTR:-:-:7101:7177
# ;Maastricht LUX HIGH:Maastricht Radar:132.350:YLH:Z:EDYY:CTR:-:-:7101:7177






with open('VATGlasses Data/VC-VR.txt') as f:
    sectors = f.readlines()

# Attempt to create random colors for every position, but in a way that also attempts to keep similar tints for similar positions types
def similarhex(position):
    import random
    if position == "APP" or position == "DEP":
        color = (0,0,random.randint(0, 255)) #"blue"
    
    elif position == "CTR":
        color = (random.randint(0, 255),140,0) #"orange"

    else:
        color = (0,random.randint(0, 255),0) #green

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
    tmp = {
        "callsign" : parts[1],
        "frequency" : parts[2],
        "type" : parts[6],
        "pre" : [parts[5]],
        "colours" : [{"hex": similarhex(parts[6])}]
    }

    id = parts[3]

    # Allow these position types for the new file
    if tmp["type"] != "ATIS"  and tmp["type"] != "GND" and tmp["type"] != "DEL":
        id_dict[id] = tmp 


pos_dict =  {}
pos_dict["positions"] = id_dict

print(pos_dict)

# Directly from dictionary
with open('VATGlasses Data/vc-vr.json', 'w') as outfile:
    json.dump(pos_dict, outfile)