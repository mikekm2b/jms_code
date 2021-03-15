# -*- coding: utf-8 -*-
# maiden head to lon/lat
# https://ham.stackexchange.com/questions/6114/convert-maidenhead-grid-square-to-lat-long-in-excel
__MH__ = 'FN13gd'  # used only if this py is standalone for testing.

def GetLon(ONE, THREE, FIVE):
    Lon = ''
	
    partONE = (float(ord(ONE)) - 65.0) * 20.0
    partTHREE = float(THREE) * 2.0
    partFIVE = (float(ord(FIVE)) - 97.0)/12.0
    partLAST = (1.0/24.0)-180.0

    Lon = partONE + partTHREE + partFIVE + partLAST
    Lon = round(Lon,1)

    return Lon

def GetLat(TWO, FOUR, SIX):
    Lat = ''

    partTWO = (float(ord(TWO)) - 65.0) * 10.0 
    partFOUR = float(FOUR)
    partSIX = (float(ord(SIX)) - 97.0)/24.0
    partLAST = 1.0/48.0 - 90.0

    Lat = partTWO + partFOUR + partSIX + partLAST
    Lat = round(Lat,1)   

    return Lat

def main(strMaidenHead = __MH__):
    if len(strMaidenHead) < 6: strMaidenHead = __MH__

    ONE = strMaidenHead[0:1]
    TWO = strMaidenHead[1:2]
    THREE = strMaidenHead[2:3]
    FOUR = strMaidenHead[3:4]
    FIVE = strMaidenHead[4:5]
    SIX = strMaidenHead[5:6]

    Lon = GetLon(ONE, THREE, FIVE)
    Lat = GetLat(TWO, FOUR, SIX)

    print ('Lon = ' + str(Lon))
    print ()
    print ('Lat = ' + str(Lat))

    return Lon, Lat

#BEGIN
if __name__ == '__main__':
    main ()
    sys.exit ('end of script: '+ os.path.basename(__file__) + os.linesep)
#END