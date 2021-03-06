"""make names of objects inot single words, so that they can be selected with a double click."""
# usage below

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/HVACTemplate-5ZoneFanCoil.idf"
outname = "../idffiles/HVACTemplate-5ZoneFanCoil1.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

changes = {}
for j, key in enumerate(data.dtls):
    items = data.dt[key]
    for item in items:
        name = item[1]
        newname = name.replace(' ', '_')
        newname = newname.replace('-', '__')
        if (name.count(' ') > 0) or (name.count('-') > 0):
            if commdct[j][1]['field'][0] == 'Name': # only name fields are changed
                changes[name] = newname
                item[1] = newname
# TODO : if changes.values() has duplicate names -> abort with message - not needed.

for key in data.dtls:
    items = data.dt[key]        
    for item in items:
        for i, field in enumerate(item):
            try:
                item[i] = changes[field]
            except KeyError, e:
                pass

open(outname, 'w').write(`data`)
