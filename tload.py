
import sqlite3
from decimal import *
# create a database

# This program requires Python3.14 (maybe it works on older systems.
# give it a try!

import csv
import sys
import re

atom = {'Jan':'01', 'Feb':'02', 'Mar':'03',
        'Apr':'04', 'May':'05', 'Jun':'06',
        'Jul':'07', 'Aug':'08', 'Sep':'09',
        'Oct':'10', 'Nov':'11', 'Dec':'12'}

# test for 01/02/2000
dmy = re.compile(r"(\d\d)/(\d\d)/(\d\d\d\d)")
mth = re.compile(r"(\d\d) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d\d\d\d)")
iso = re.compile(r"\d\d\d\d-\d\d-\d\d")
def adj_date(dt):
    """standardise the date"""
    mt1 = dmy.fullmatch(dt)  # 01/07/2028
    mt2 = mth.fullmatch(dt)  # 01 Jul 2028
    mt3 = iso.fullmatch(dt)  # 2028-07-01
    if mt1:
        rt = mt1.group(3)+'-'+mt1.group(2)+'-'+mt1.group(1)
    elif mt2:
        rt = mt2.group(3)+'-'+atom[mt2.group(2)]+'-'+mt2.group(1)
    elif mt3:
        # already in iso format
        rt = dt
    else:
        rt = 'no match'
    return rt

def testelements(r):
    """ return True if a valid header"""
    p = ['Date','Type','Description','Value','Balance','Account Name','Account Number']
    if len(p) != len(r):
        print("Number of elements in header does not match")
        sys.exit(1)
    for ix in range(0,len(r)):
        if r[ix] != p[ix]:
            print("Mismatch in header")
            sys.exit(1)
    return True

def format_number(n):
    """ format a number into nnnn.dd"""
    return('{0:.02f}'.format(Decimal(n)))

### end of subroutines ######################

P = ['Date','Type','Description','Value','Balance','Account Name','Account Number']

connection = sqlite3.connect("trans.db")
cur = connection.cursor()


############# NOTE: using 65 bit float, not char float  ########
cur.execute("""CREATE TABLE IF NOT EXISTS tr (
    date CHAR, type CHAR, description CHAR, value FLOAT,
    balance FLOAT, name CHAR, number CHAR

    )    """)

with open('testme.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    line = 0
    headerseen = False
    for row in spamreader:
        line = line + 1
        if len(row) == 0:
            continue
        if headerseen == False and line < 4:
            if testelements(row):
                headerseen = True
                continue
        if headerseen:
            print('orignal:', row)
            row[0] = adj_date(row[0])
            print('new    :', row)
#            print(row[3], row[4])
#            print(type(row[3]))
            row[3] = format_number(row[3])
#            print(type(row[3]))
            row[4] = format_number(row[4])
            cur.execute("""INSERT INTO tr VALUES(?,?,?,?,?,?,?) """, row)

connection.commit()
connection.close()




        
    

