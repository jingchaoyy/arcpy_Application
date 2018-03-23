# After running the evacuation tool, evacuation routes and
# closets exits can be visualized here

# Jingchao, Patrick
# 11/28/2017

from Tkinter import *
import struct


# define point, polyline classes
class Point:
    # deinfe object initialization method
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Polyline:
    # deinfe object initialization method
    def __init__(self, points=[], partsNum=0, partsIndex=0):
        self.points = points
        self.partsNum = partsNum
        self.partsIndex = partsIndex

# open index file to read in binary mode
Neighborhood_Clusters = 'C:\Users\/no281\PycharmProjects\Final\Neighborhood_Clusters\Neighborhood_Clusters'
Emergency_Walkout_Routes = 'C:\Users\/no281\PycharmProjects\Final\Emergency_Walkout_Routes\Emergency_Walkout_Routes'
Regional_Evacuation_Routes = 'C:\Users\/no281\PycharmProjects\Final\Regional_Evacuation_Routes\evaRoutesInDC'
DC_Roads = 'C:\Users\/no281\PycharmProjects\Final\Street_Centerlines\Street_Centerlines'

bikeShareLocation = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\/bikeLocaInDC'
userLocation = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\incident'
evacuationExit = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\evacuationExit'

RoutestoBike = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\RoutestoBike'
ClosestBike = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\ClosestBike'
RoutestoExit = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\RoutestoExit'
ClosestExit = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\ClosestExit'

Routes_allBiketoExit = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\Routes_allBiketoExit'
Routes_usertoExit = 'C:\Users\/no281\PycharmProjects\Final\Final_Project\Routes_usertoExit'

# Capital_Bike_Share_Locations = 'C:\Users\/no281\PycharmProjects\Final\Capital_Bike_Share_Locations\Capital_Bike_Share_Locations'

# create main window object
root = Tk()
# create canvas object
can = Canvas(root, width=1030, height=950)


def readShpPoint(fileName, ratio, color, minX, maxY):  # parameter fileName is the pathfile name without extension
    fileName = fileName + '.shp'
    shpFile = open(fileName, 'rb')
    s = shpFile.seek(24)
    s = shpFile.read(4)
    b = struct.unpack('>i', s)
    featNum = (b[0] * 2 - 100) / 28
    s = shpFile.read(72)
    header = struct.unpack("<iidddddddd", s)
    # minx, miny, maxx, maxy = header[2], header[3], header[4], header[5]
    points= []
    for i in range(0, featNum):
        shpFile.seek(100 + 12 + i * 28)
        s = shpFile.read(16)
        x, y = struct.unpack('dd', s)
        point = Point(x, y)
        points.append(point)

    xylist = []  # define an empty xylist for holding converted coordinates
    for p in points:
        # print (point.x, point.y)
        winX = (p.x - minX) / ratio
        winY = - (p.y - maxY) / ratio
        xylist.append(Point(winX,winY))
        #xylist.append(Point(winY))

    for i in xylist:
        can.create_oval(i.x - 3.5, i.y - 3.5, i.x + 3.5, i.y + 3.5, fill= color)

    shpFile.close()

def drwaShp(fileName, ratio, color, minX, minY, maxX, maxY):
    # ----Part 1: read and process the first 100 bytes
    # read index file header and interpret the meta information. e.g., bounding box, and # of #records
    indexName = fileName + '.shx'
    shxFile = open(indexName, "rb")
    s = shxFile.read(28)  # read first 28 bytes
    # convert into 7 integers

    # get file length
    header = struct.unpack('>iiiiiii', s)
    fileLength = header[len(header) - 1]

    # calcualate polyline numbers in the shape file based on index file length
    polylineNum = int((fileLength * 2 - 100) / 8)

    # read other 72 bytes in header
    s = shxFile.read(72)
    # convert into values
    header = struct.unpack('<iidddddddd', s)
    # get boundingbox for the shape file
    if minX == 0 and minY == 0 and maxX == 0 and maxY == 0:
        minX, minY, maxX, maxY = header[2], header[3], header[4], header[5]

    # read records meta information, such as offset,
    # and content length for each records,

    # define an empty list for holding offset of each feature in main file
    recordsOffset = []
    # loop through each feature
    for i in range(polylineNum):
        # jump to beginning of each record
        shxFile.seek(100 + i * 8)
        # read out 4 bytes as offset
        s = shxFile.read(4)
        offset = struct.unpack('>i', s)
        # keep the offset in the list
        recordsOffset.append(offset[0] * 2)

    shxFile.close()  # close the index file

    # ----Part2. read each polyline and prepare them in right order
    # open the main file for read in binary
    shpFile = open(fileName+'.shp', 'rb')
    # shapefile name can be replaced with any polyline

    polylines = []  # define an empty list for polylines

    # loop through each offset of all polylines
    for offset in recordsOffset:
        # define two lists for holding values
        x, y = [], []
        # jump to partsNum and pointsNum of the polyline and read them out
        shpFile.seek(offset + 8 + 36)
        s = shpFile.read(8)
        polyline = Polyline()  # generate an empty polyline object
        partsNum, pointsNum = struct.unpack('ii', s)
        polyline.partsNum = partsNum
        # print ('partsNum, pointsNum:', partsNum, pointsNum)
        s = shpFile.read(4 * partsNum)
        str = ''
        for i in range(partsNum):
            str = str + 'i'

        # get the starting point number of each part and keep in a partsIndex list
        polyline.partsIndex = struct.unpack(str, s)

        points = []
        for i in range(pointsNum):
            # read out polyline coordinates
            s = shpFile.read(16)
            x, y = struct.unpack('dd', s)

            # read the coordinates values
            # assemble data into objects of points, polyline, and polygon or other types
            point = Point(x, y)
            points.append(point)
        # assign points lists to the polyline
        polyline.points = points
        # add the polyline read to the
        polylines.append(polyline)


    shpFile.close()

    # ----Part 3: prepare to visualize the data
    # define wondow size
    windowWidth, windowHeight = 1000, 1000

    # calculate ratio for visualization
    ratiox = (maxX - minX) / windowWidth
    ratioy = (maxY - minY) / windowHeight

    # take the smaller ratio
    if ratio == 0:
        ratio = min(ratiox,ratioy)

    for polyline in polylines:
        xylist = []  # define an empty xylist for holding converted coordinates

        # loop through each point
        # and calculate the window coordinates, put in xylist
        for point in polyline.points:
            # print (point.x, point.y)
            winX = (point.x - minX) / ratio
            winY = - (point.y - maxY) / ratio
            xylist.append(winX)
            xylist.append(winY)
        # print "xylist: ",xylist

        for k in range(polyline.partsNum):  # visualize each part separately
            if (k == polyline.partsNum - 1):
                endPointIndex = len(polyline.points)
            else:
                endPointIndex = polyline.partsIndex[k + 1]

            # define a temporary list for holding the part coordinates
            tempXYlist = []

            for m in range(polyline.partsIndex[k], endPointIndex):
                # polyline.partsIndex[k]:the first point in this part
                # endPointIndex:the last point in this part
                tempXYlist.append(xylist[(m * 2)])
                tempXYlist.append(xylist[(m * 2 + 1)])
            # print "tempXYList: ",tempXYlist

            # create the line
            can.create_line(tempXYlist, width = 2, fill=color)
            # lines.append(tempXYlist)
            # can.create_line(lines, fill='blue')
    # can.pack()
    # root.mainloop()

    return ratio, minX, minY, maxX, maxY

# r = drwaShp(Neighborhood_Clusters,0,'gray')
# print 'ratio',r
rr = drwaShp(DC_Roads,0,'#bfbfbf',0,0,0,0)
print 'ratio',rr[0]
ee = readShpPoint(evacuationExit,rr[0],'red',rr[1],rr[4])
ewr = drwaShp(Emergency_Walkout_Routes,rr[0],'#ffbf00',rr[1],rr[2],rr[3],rr[4])
#print 'ratio',ewr[0]
rer = drwaShp(Regional_Evacuation_Routes,rr[0],'#ff6699',rr[1],rr[2],rr[3],rr[4])
#print 'ratio',rer[0]
bsl = readShpPoint(bikeShareLocation,rr[0],'#0099cc',rr[1],rr[4])


"""
    visualization option 1:
    for all the user location to their nearest bike share locations,
    then from the selected bike share location to their nearest exit
"""
# ul = readShpPoint(userLocation,rr[0],'black',rr[1],rr[4])
# cb = readShpPoint(ClosestBike,rr[0],'#ff0000',rr[1],rr[4])
# ce = readShpPoint(ClosestExit,rr[0],'#ff0000',rr[1],rr[4])
# rtb = drwaShp(RoutestoBike,rr[0],'#00ff99',rr[1],rr[2],rr[3],rr[4])
# rte = drwaShp(RoutestoExit,rr[0],'#00ff99',rr[1],rr[2],rr[3],rr[4])

print 'visualization finished'

"""
    visualization option 2:
    for all the bike share locations to their nearest exit
"""
# rbe = drwaShp(Routes_allBiketoExit,rr[0],'#00ff99',rr[1],rr[2],rr[3],rr[4])

"""
    visualization option 3:
    for the direct out routes from a user
"""
ul2 = readShpPoint(userLocation,rr[0],'black',rr[1],rr[4])
rue = drwaShp(Routes_usertoExit,rr[0],'#00ff99',rr[1],rr[2],rr[3],rr[4])


# can.create_line(700, 20, 800, 20, fill='green', width=2, tags='line1')
# can.create_line(700, 30, 800, 30, fill='red', width=2, tags='line2')
# can.create_line(700, 40, 800, 40, fill='blue', width=2,tags='line3')


can.pack()
root.mainloop()
