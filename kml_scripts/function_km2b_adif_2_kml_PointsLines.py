# Module Functional Use
# Module Author:  KM2B, Mike
# Enables generation of KML file for google maps and earth of Amateur Radio contacts.
# Tested for fixed station use, but, should adapt to mobil use.  

# Module import dependencies.
# This kml creator from .adi file of Amateur Radio contacts requires four dependencies

# 1) simplekml module from whl file at reference  
#    https://pypi.python.org/pypi/simplekml

# 2) OK4BX_adif.py adapted by me from references below.
#    http://web.bxhome.org/blog/ok4bx/2012/05/adif-parser-python'  
#    https://web.bxhome.org/content/adifpy (fix problem with z)
#    Parses the adif file into a python dictionary.  

# 3) grid6_longlat.py, adapted by me from references below.
#    https://ham.stackexchange.com/questions/6114/convert-maidenhead-to-lat-long-in-excel/6122 
#    Computes longitude and lattitude for each contact based on 6 character gridsquare

# 4) grid4_longlat.py
#    https://ham.stackexchange.com/questions/6114/convert-maidenhead-to-lat-long-in-excel/6122 
#    Computes longitude and lattitude for each contact based on 4 character gridsquare


import sys
import io

import simplekml

import OK4BX_adif   

import grid4_longlat
import grid6_longlat  

import argparse

def remove_nonascii(file_name):
    ascii_fn = file_name + '.ascii'
    with io.open(file_name,'r',encoding='utf-8',errors='ignore') as infile, \
        io.open(ascii_fn,'w',encoding='ascii',errors='ignore') as outfile:
        for line in infile:
            print(*line.split(), file=outfile)
    return ascii_fn

def init_variables(adif):
    num = len(adif)
    kml = simplekml.Kml()

    print('********* Making Points To Lines KML ****************')

    print('*** PART 2:  Making Line KML *******')
    # Set up for making lines kml by obtaining My Call Lon Lat
    # Obtain Lon, Lat for My Call for Line building.
    # Parse the myGrid into 1-4 letters
    nogridlist =[]
    numcontacts = 0
    return num,kml,nogridlist,numcontacts


def make_qso_kmlpoint(adif,kml,nogridlist,numcontacts,i):
    hisGrid =[] # so holdover grid square from previous call is not carried forward.

    # Extract adif dictionary to one line for lon/at calc 

    line=adif[i]
        
    try:
        hisCall = line['call']
    
        try:
            myCall = line['station_callsign']
            #myCall = 'KM2B'
        except:
            myCall = 'KM2B'


        myGrid = 'FN13gd'


        try:
            hisGrid = line['gridsquare']

            # HISGRID Lon/Lat Section
            # Parse the hisGrid into 1-4 letters
            if (len(hisGrid) == 4):
                gridSq = hisGrid
                ONE = gridSq[0:1]
                TWO = gridSq[1:2]
                THREE = gridSq[2:3]
                FOUR = gridSq[3:4]
                
                # Get hisGrid Longtitude and Lattitude
                hisLon = grid4_longlat.GetLon(ONE, THREE)
                hisLat = grid4_longlat.GetLat(TWO, FOUR)

                # Print during debug phase
                print (hisCall)
                print ('Longitude = ' + str(hisLon))
                print ('Lattitude = ' + str(hisLat) + '\n')
            elif(len(hisGrid) == 6):
                gridSq = hisGrid
                ONE = gridSq[0:1]
                TWO = gridSq[1:2]
                THREE = gridSq[2:3]
                FOUR = gridSq[3:4]
                FIVE = gridSq[4:5]
                SIX  = gridSq[5:6]
                
                # Get hisGrid Longtitude and Lattitude
                hisLon = grid6_longlat.GetLon(ONE, THREE, FIVE)
                hisLat = grid6_longlat.GetLat(TWO, FOUR, SIX)

                # Print during debug phase
                print (hisCall)
                print ('Longitude = ' + str(hisLon))
                print ('Lattitude = ' + str(hisLat) + '\n')

            else:
                print('not a FOUR OR SIX character call')
                
            # MYGRID Lon/Lat Section
            gridSq = myGrid
            ONE = gridSq[0:1]
            TWO = gridSq[1:2]
            THREE = gridSq[2:3]
            FOUR = gridSq[3:4]
            FIVE = gridSq[4:5]
            SIX  = gridSq[5:6]

            # Get Longtitude and Lattitude
            myLon = grid6_longlat.GetLon(ONE, THREE, FIVE)
            myLat = grid6_longlat.GetLat(TWO, FOUR, SIX)
                
            #print (myCall)
            #print ('Longitude = ' + strMyLon)
            #print ('Lattitude = ' + strMyLat + '\n')

            # Build kml file for google maps to show lines
            height = 0
            pnt = kml.newpoint(name=hisCall, coords=[((hisLon),(hisLat))])
            # print kml
            pnt.style.iconstyle.scale = 2  #Size of icon
            # pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png'
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/orange-blank.png'
            # pnt.style.iconstyle.icon.href = 'http://labs.google.com/ridefinder/images/mm_20_yellow.png'
            linestring = kml.newlinestring(name=hisCall)
            linestring.tessellate = 1  #Necessary to draw very long lines
            linestring.coords = [(str(myLon),str(myLat),height), (str(hisLon),str(hisLat),height)]
            linestring.style.linestyle.color = simplekml.Color.white
            linestring.style.linestyle.width = 0.01

            numcontacts = numcontacts + 1

        except: 
            nogridlist.append(hisCall)

    except:
        print('****hisCall not an ASCII call sign******')
        print('record number in file', i)
        print('call sign perceived',  hisCall)
        sys.exit()
    return pnt,myCall,myLon,myLat,nogridlist,numcontacts


def make_home_kmlpoint(pnt,kml,myCall,myLon,myLat):
    pnt = kml.newpoint(name=myCall, coords=[((myLon),(myLat))]) #place on instance of myCall at my Location
    return pnt,kml


def print_noGrid_calls(nogridlist):
    print('Calls without grid squares')
    for call in nogridlist:
        print(call)


def save_kmlfile_reportSumary(file_name,kml,numcontacts):
    print('Saving kml file')
    kml.save(file_name + '.kml')
    print('')
    print ('SUCCESS')
    print ('number of contacts = ' + str(numcontacts))
    print (file_name + '.kml written to directory')
    print ('You can now upload the .kml file to google maps or google earth')
    return




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="MUST be an .adif or .adi file format")
    args = parser.parse_args()

    file_name  = args.filename

    ascii_fn = remove_nonascii(file_name)
    
    adif = OK4BX_adif.parse(ascii_fn)
    
    num,kml,nogridlist,numcontacts=init_variables(adif)

    for i in range(0, num, 1):
        pnt,myCall,myLon,myLat,nogridlist,numcontacts = make_qso_kmlpoint(adif,kml,nogridlist,numcontacts,i)

    pnt,kml= make_home_kmlpoint(pnt,kml,myCall,myLon,myLat)

    print_noGrid_calls(nogridlist)

    save_kmlfile_reportSumary(file_name,kml,numcontacts)


if __name__ == "__main__":
    main()



