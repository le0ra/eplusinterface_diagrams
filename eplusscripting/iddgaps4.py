"""idd comments have gaps in them.
With \note fields as indicated
This code fills those gaps
see: SCHEDULE:DAY:LIST as an example"""

# works for all objects, including troublesome ones

# idd might look like this
# <snip>
# / field varA 1
# / field varB 1
# / field varC 1
# / field varA 2
# / field varB 2
# / field varC 2
# / above pattern continues
# - 
# find objects where the fields are not named
# do the following only for those objects
# find the first field that has an integer. This is a repeating field
# gather the repeating field names (without the integer)
# generate all the repeating fields for all variables



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
# find objects where all the fields are not named
gkeys = [dtls[i] for i in range(len(dtls)) if commdct[i].count({}) > 2]

nofirstfields = []
wierdfirstfield = []
# operatie on those fields
for key_txt in gkeys:
    # print key_txt
    # for a function, pass comm as a variable
    key_i = dtls.index(key_txt.upper())
    comm = commdct[key_i]



    # get all fields
    fields = getfields(comm)
    
    # get repeating field names
    repnames = repeatingfieldsnames(fields)
    
    try:
        first = repnames[0][0] % (1, )
    except IndexError, e:
        nofirstfields.append(key_txt)
        continue
    # print first

    # get all comments of the first repeating field names
    firstnames = [repname[0] % (1, ) for repname in repnames]
    fcomments = [field for field in fields if bunchhelpers.onlylegalchar(field['field'][0]) in firstnames]
    fcomments = [dict(fcomment) for fcomment in fcomments]
    for cm in fcomments:
        fld = cm['field'][0]
        fld = bunchhelpers.onlylegalchar(fld)
        fld = bunchhelpers.replaceint(fld)
        cm['field'] = [fld]

    for i, cm in enumerate(comm[1:]):
        thefield = cm['field'][0]
        thefield = bunchhelpers.onlylegalchar(thefield)
        if thefield == first:
            break
    first_i = i + 1

    newfields = []
    for i in range(1, len(comm[first_i:]) / len(repnames) + 1):
        for fcomment in fcomments:
            nfcomment = dict(fcomment)
            fld = nfcomment['field'][0]
            fld = fld % (i, )
            nfcomment['field'] = [fld]
            newfields.append(nfcomment)

    try:
        for i, cm in enumerate(comm):
            if i < first_i:
                continue
            else:
                afield = newfields.pop(0)
                comm[i] = afield
    except IndexError, e:
        wierdfirstfield.append(key_txt)
        continue
    commdct[key_i] = comm
 
 
afield = 'afield %s'
for key_txt in nofirstfields + wierdfirstfield:
    key_i = dtls.index(key_txt.upper())
    comm = commdct[key_i]
    for i, cm in enumerate(comm):
        if cm == {}:
            first_i = i
            break
    for i, cm in enumerate(comm):
        if i >= first_i:
            comm[i]['field'] = afield % (i - first_i +1,)
    
# for key_txt in nofirstfields:
#     print key_txt
# print '-'    
# for key_txt in wierdfirstfield:
#     print key_txt
key_txt = "TABLE:MULTIVARIABLELOOKUP"    
key_i = dtls.index(key_txt.upper())
comm = commdct[key_i]
#     
print comm