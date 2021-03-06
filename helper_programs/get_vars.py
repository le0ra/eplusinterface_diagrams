"""get the variable list
Usage:
python get_vars.py fname ReportVariableDataDictionaryIndex
python get_vars.py a.sql 6
func and year are hard coded
# TODO: alow it to get multiple variables
"""
import sys
import getopt


import eplussql
import date_functions

help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


# fname = "./eplussql_test/eplussql.sql"
# ReportVariableDataDictionaryIndex = 6
# year = 2001  
# func = None      
# func = eplussql.c2f

def printvars(fname, ReportVariableDataDictionaryIndex, func=None, year=2001):
    """print the variables in csv format"""
    cursor = eplussql.getcursor(fname)
    varname = eplussql.get_variablename(cursor,
                        ReportVariableDataDictionaryIndex)
    keyvalue = eplussql.get_keyvalue(cursor,
                        ReportVariableDataDictionaryIndex)
    matrix = eplussql.get_variables(cursor, 
            ReportVariableDataDictionaryIndex, func=func)
    yhours = date_functions.yeardateshours(year)  
    outmat = [["datetime", varname]] + [["", keyvalue]] + zip(yhours, matrix)      
    for row in outmat:
        print "%s, %s" % tuple(row)
 
 
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
        fname, ReportVariableDataDictionaryIndex = args
        year = 2001  
        func = None      
        # func = eplussql.c2f
        printvars(fname, ReportVariableDataDictionaryIndex, 
                            func=func, year=year)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
