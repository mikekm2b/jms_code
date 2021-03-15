# -*- coding: utf-8 -*-
# maiden head to lon/lat
# https://ham.stackexchange.com/questions/6114/convert-maidenhead-to-lat-long-in-excel/6122

def GetLon(ONE, THREE):
    Lon = ''
	
    Field = ((ord(ONE.lower()) - 97) * 20) 
    Square = int(THREE) * 2

    Lon = (Field + Square - 180 )

    return Lon

def GetLat(TWO, FOUR):
    Lat = ''
	
    Field = ((ord(TWO.lower()) - 97) * 10) 
    Square = int(FOUR)

    Lat = (Field + Square - 90)

    pass

    return Lat

def mh2ll(strGridSquare):

    ONE = strGridSquare[0:1]
    TWO = strGridSquare[1:2]
    THREE = strGridSquare[2:3]
    FOUR = strGridSquare[3:4]

    (strLon) = GetLon(ONE, THREE)
    (strLat) = GetLat(TWO, FOUR)

    print ('Longitude = ' + strLon)

    print ('\nLattitude = ' + strLat + '\n')

    return strLon, strLat
