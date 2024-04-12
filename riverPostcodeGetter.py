import postcodes_io_api
import numpy
from pyproj import Transformer
from pathlib import Path
import xml.etree.ElementTree as ET
import os

#extracts .gml file as an xml object interpretable by python 
def getXML(filePath):
    return ET.parse(filePath).getroot()
 
#converts the coordinates from strings to floats 
def stringToFloat(sCoords):
    return [float(i) for i in sCoords]       

#request a list of all postcodes within a radius, r, of given lat long coordinates 
def getPostcodes(api, coordinates, r):
    lat = coordinates[0]
    lng = coordinates[1]
    return api.get_nearest_postcodes_for_coordinates(latitude=lat, longitude=lng, radius=r)

#remove any empty entries from the list of postcodes
def cleanPostcodes(pcs):
    cleanedPostcodes = []
    for text in pcs:
        if text['result'] == None:
            continue
        else:
            locations = text['result']
            for l in locations:
                cleanedPostcodes.append(l['postcode'])
                
    return cleanedPostcodes

#converts British National Grid coordinates to EPSG:4326
def coordsToLatLong(coords, coordSystem):
    lat = coords[0]
    lng = coords[1]
    t = Transformer.from_crs(coordSystem, "EPSG:4326")
    return t.transform(lat, lng)

#saves a list of the coordinates to a text file
def saveCoordinates(riverName, coordinateList):
    coordinateText = ""
    for coords in coordinateList:
        coordinateText += str(coords[0]) + "," + str(coords[1]) + ',#00FF00,marker,"Mumbai"\n'
        
    file =  open("{rn} coordinate list.txt".format(rn=riverName), "w")
    file.write(coordinateText)
    
#radius around coordinates to search (metres)    
searchRadius = 1500 

#name of river you want the coordinates of 
riverName = "Afon Gwy" 

#name of .gml file
inputFileName = "OSOpenRivers.gml" 

#name of the output file 
outputFileName = "{rn} Postcode Data.csv".format(rn=riverName) 

#This contains the coordinate system used by your .gml file, the default is for BNG so you'll need to change this depending on your data
coordSystem = "EPSG:27700"

#flag used to decide if the lat long coordinates should be saved to a text file
saveDrawCoords = False


#define the api used to request postcodes from
api = postcodes_io_api.Api(debug_http=True)

#loads
currentDirectory = Path().parent.absolute()
filePath = os.path.join(currentDirectory, inputFileName)
root = getXML(filePath)

riverList = root[2][0][2]

namespaces = {"river": "http://namespaces.os.uk/Open/Rivers/1.0"}
print("Searching for river nodes...\n")

#find all nodes of the river 
riverNodes = root.findall(".//*/*[river:watercourseName='{rn}']".format(rn=riverName), namespaces)
print("River nodes located\n")
coordinateStrings = [node[2][0][0].text.split() for node in riverNodes]
coordinateFloats = []

#convert coordinates to floating points 
for coordinates in coordinateStrings:
    floatCoords = stringToFloat(coordinates)
    floatCoordPairs = [floatCoords[i:i+2] for i in range(0, len(floatCoords), 2)]
    coordinateFloats.append(floatCoordPairs)

latLongCoords= []

#convert coords to lat long 
for coordinatePair in coordinateFloats:
    for i in coordinatePair:
        latLongCoords.append(coordsToLatLong(i, coordSystem))

print("Obtained latitude and longitude\n")    

print("Requesting postcodes from API...\n")

progressTracker = 1
postcodes = []

#obtain postcodes using lat long coordinates by calling the postcodes.io API
for i in latLongCoords:
    postcodes.append(getPostcodes(api, i, searchRadius))
    print("Current Progress: {prog}%".format(prog=progressTracker/len(latLongCoords) * 100))
    progressTracker += 1

print("Finished obtaining postcodes")

#remove null entries and any duplicate postcodes
cleanedPostcodes = cleanPostcodes(postcodes)
outpuData = list(dict.fromkeys(cleanedPostcodes))

#saves postcodes as rows in a csv file 
numpy.savetxt(outputFileName, outpuData, delimiter=",", fmt="%s")

if saveDrawCoords == True:
    saveCoordinates(riverName, latLongCoords)
