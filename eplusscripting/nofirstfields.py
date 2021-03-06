"""in commdct if there is no first field in the repeating fields
Code is needed to add fields to the repeating fields"""

import sys
from pprint import pprint
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

import bunchhelpers

def getfields(comm):
    """get all the fields that have the key 'field' """
    fields = []
    for field in comm:
        if field.has_key('field'):
            fields.append(field)
    return fields
    
def repeatingfieldsnames(fields):
    """get the names of the repeating fields"""
    fnames = [field['field'][0] for field in fields]
    fnames = [bunchhelpers.onlylegalchar(fname) for fname in fnames]
    fnames = [fname for fname in fnames if bunchhelpers.intinlist(fname.split())]
    fnames = [(bunchhelpers.replaceint(fname), None) for fname in fnames]
    dct = dict(fnames)
    repnames = fnames[:len(dct.keys())]
    return repnames
    

# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
commdct = bunchhelpers.cleancommdct(commdct)

dt = data.dt
dtls = data.dtls

afield = 'afield %s'
key_txt = 'MATERIALPROPERTY:GLAZINGSPECTRALDATA'
key_txt = 'TABLE:MULTIVARIABLELOOKUP'
key_i = dtls.index(key_txt.upper())
comm = commdct[key_i]


for i, cm in enumerate(comm):
    if cm == {}:
        first_i = i
        break
print first_i
for i, cm in enumerate(comm):
    if i >= first_i:
        comm[i]['field'] = afield % (i - first_i +1,)
print comm[20:40]       