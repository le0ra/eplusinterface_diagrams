""" copyt of airloop.py
make airloop diagrams. 
draws the simplest diagram. 
Does not draw the contents of the branch

try to get uncontrolled working"""

import pydot
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import loops


iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/HVACTemplate-5ZonePackagedVAV_exp.idf" # for supply mixer and return plenum
fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # for supply plenum
fname = "../idffiles/VAVSingleDuctReheat.idf" # for zone mixer
# fname = "../idffiles/DualDuctConstVolDamper.idf" # for zone mixer
fname = "../idffiles/06_OneStorey_Radiant_5.idf" # metrovalley
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


# Get the demand and supply nodes from 'airloophvac'
# in airloophvac get:
#   get branch, supplyinlet, supplyoutlet, demandinlet, demandoutlet
objkey = "airloophvac".upper()
fieldlists = [["Branch List Name",
    "Supply Side Inlet Node Name",
    "Demand Side Outlet Node Name",
    "Demand Side Inlet Node Names",
    "Supply Side Outlet Node Names"]] * loops.objectcount(data, objkey)
airloophvacs = loops.extractfields(data, commdct, objkey, fieldlists)
# airloophvac = airloophvacs[0]

# in AirLoopHVAC:ZoneSplitter:
#   get Name, inlet, all outlets
objkey = "AirLoopHVAC:ZoneSplitter".upper()
singlefields = ["Name", "Inlet Node Name"]
fld = "Outlet %s Node Name"
repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
zonesplitters = loops.extractfields(data, commdct, objkey, fieldlists)

# in AirLoopHVAC:SupplyPlenum:
#   get Name, Zone Name, Zone Node Name, inlet, all outlets
objkey = "AirLoopHVAC:SupplyPlenum".upper()
singlefields = ["Name", "Zone Name", "Zone Node Name", "Inlet Node Name"]
fld = "Outlet %s Node Name"
repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
supplyplenums = loops.extractfields(data, commdct, objkey, fieldlists)

# in AirLoopHVAC:ZoneMixer:
#   get Name, outlet, all inlets
objkey = "AirLoopHVAC:ZoneMixer".upper()
singlefields = ["Name", "Outlet Node Name"]
fld = "Inlet %s Node Name"
repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
zonemixers = loops.extractfields(data, commdct, objkey, fieldlists)

# in AirLoopHVAC:ReturnPlenum:
#   get Name, Zone Name, Zone Node Name, outlet, all inlets
objkey = "AirLoopHVAC:ReturnPlenum".upper()
singlefields = ["Name", "Zone Name", "Zone Node Name", "Outlet Node Name"]
fld = "Inlet %s Node Name"
repeatfields = loops.repeatingfields(data, commdct, objkey, fld)
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
returnplenums = loops.extractfields(data, commdct, objkey, fieldlists)


# connect room to each equip in equiplist
# in ZoneHVAC:EquipmentConnections:
#   get Name, equiplist, zoneairnode, returnnode
objkey = "ZoneHVAC:EquipmentConnections".upper()
singlefields = ["Zone Name", "Zone Conditioning Equipment List Name", 
    "Zone Air Node Name", "Zone Return Air Node Name"]
repeatfields = []
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
equipconnections = loops.extractfields(data, commdct, objkey, fieldlists)
# in ZoneHVAC:EquipmentList:
#   get Name, all equiptype, all equipnames
objkey = "ZoneHVAC:EquipmentList".upper()
singlefields = ["Name", ]
fieldlist = singlefields
flds = ["Zone Equipment %s Object Type", "Zone Equipment %s Name"]
repeatfields = loops.repeatingfields(data, commdct, objkey, flds)
fieldlist = fieldlist + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
equiplists = loops.extractfields(data, commdct, objkey, fieldlists)
equiplistdct = dict([(ep[0], ep[1:])  for ep in equiplists])
for key, equips in equiplistdct.items():
    enames = [equips[i] for i in range(1, len(equips), 2)]
    equiplistdct[key] = enames
# adistuunit -> room    
# adistuunit <- VAVreheat 
# airinlet -> VAVreheat
# in ZoneHVAC:AirDistributionUnit:
#   get Name, equiplist, zoneairnode, returnnode
objkey = "ZoneHVAC:AirDistributionUnit".upper()
singlefields = ["Name", "Air Terminal Object Type", "Air Terminal Name"]
repeatfields = []
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
adistuunits = loops.extractfields(data, commdct, objkey, fieldlists)
# for each AirTerminal:
#     for this AirTerminal
#         get Name, airinletnode
adistuinlets = loops.makeadistu_inlets(data, commdct)
alladistu_comps = []
for key in adistuinlets.keys():
    objkey = key.upper()
    singlefields = ["Name"] + adistuinlets[key]
    repeatfields = []
    fieldlist = singlefields + repeatfields
    fieldlists = [fieldlist] * loops.objectcount(data, objkey)
    adistu_components = loops.extractfields(data, commdct, objkey, fieldlists)
    alladistu_comps.append(adistu_components)

# in AirTerminal:SingleDuct:Uncontrolled:
#   get Name, airinletnode
objkey = "AirTerminal:SingleDuct:Uncontrolled".upper()
singlefields = ["Name", "Zone Supply Air Node Name"]
repeatfields = []
fieldlist = singlefields + repeatfields
fieldlists = [fieldlist] * loops.objectcount(data, objkey)
uncontrolleds = loops.extractfields(data, commdct, objkey, fieldlists)


#---------

edges = []

# connect demand and supply side
for airloophvac in airloophvacs:
    supplyinlet = airloophvac[1]
    supplyoutlet = airloophvac[4]
    demandinlet = airloophvac[3]
    demandoutlet = airloophvac[2]
    # edges = [supplyoutlet -> demandinlet, demandoutlet -> supplyinlet]
    moreedges = [(supplyoutlet, demandinlet), (demandoutlet, supplyinlet)]
    edges = edges + moreedges

# connect zonesplitter to nodes
for zonesplitter in zonesplitters:
    name = zonesplitter[0]
    inlet = zonesplitter[1]
    outlets = zonesplitter[2:]
    edges.append((inlet, name))
    for outlet in outlets:
        edges.append((name, outlet))

# connect supplyplenum to nodes
for supplyplenum in supplyplenums:
    name = supplyplenum[0]
    inlet = supplyplenum[3]
    outlets = supplyplenum[4:]
    edges.append((inlet, name))
    for outlet in outlets:
        edges.append((name, outlet))

# connect zonemixer to nodes
for zonemixer in zonemixers:
    name = zonemixer[0]
    outlet = zonemixer[1]
    inlets = zonemixer[2:]
    edges.append((name, outlet))
    for inlet in inlets:
        edges.append((inlet, name))

# connect returnplenums to nodes
for returnplenum in returnplenums:
    name = returnplenum[0]
    outlet = returnplenum[3]
    inlets = returnplenum[4:]
    edges.append((name, outlet))
    for inlet in inlets:
        edges.append((inlet, name))

# connect room to return node
for equipconnection in equipconnections:
    zonename = equipconnection[0]
    returnnode = equipconnection[-1]
    edges.append((zonename, returnnode))
    
# connect equips to room
for equipconnection in equipconnections:
    zonename = equipconnection[0]
    zequiplistname = equipconnection[1]
    for zequip in equiplistdct[zequiplistname]:
        edges.append((zequip, zonename))

# adistuunit <- adistu_component 
for adistuunit in adistuunits:
    unitname = adistuunit[0]
    compname = adistuunit[2]
    edges.append((compname, unitname))

# airinlet -> adistu_component
for adistu_comps in alladistu_comps:
    for adistu_comp in adistu_comps:
        name = adistu_comp[0]
        for airnode in adistu_comp[1:]:
            edges.append((airnode, name))

# supplyairnode -> uncontrolled
for uncontrolled in uncontrolleds:
    name = uncontrolled[0]
    airnode = uncontrolled[1]            
    edges.append((airnode, name))
                
# get all branches
branchkey = "branch".upper()
branches = data.dt[branchkey]
branch_i_o = {}
for br in branches:
    br_name = br[1]
    in_out = loops.branch_inlet_outlet(data, commdct, br_name)
    branch_i_o[br_name] = dict(zip(["inlet", "outlet"], in_out))
for br_name, in_out in branch_i_o.items():
    edges.append((in_out["inlet"], br_name))
    edges.append((br_name, in_out["outlet"]))
#---------

# make graph
g=pydot.graph_from_edges(edges, directed=True) 
g.write('a.dot')
g.write_png('a.png')