# This tool mainly focus on how to use network analysis to find
# the closest evacuation exit in D.C. area base on a user location,
# and the data used here can be replaced

# Jingchao
# 11/28/2017

import arcpy

# setting up the environment for arcpy
arcpy.env.workspace = "C:\Users\/no281\PycharmProjects\Final\Final_Project\/final_DCEvacuation.gdb"
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("network")

# in this demo, the closest facilities will be calculated only based on distance
measurement_units = "Meters"
networkDataset = r'DC_Roads_ND_ND'
# output path
outputGeodatabase = r'C:\Users\/no281\PycharmProjects\Final\Final_Project\/final_DCEvacuation.gdb'

# Set local variables
incidents1 = r'incident'
facilities1 = r'bikeLocaInDC'
# contain route from incidents to closest bike share location
outputRoutesName1 = "RoutestoBike"
outputDirectionsName1 = "DirectionstoBike"
# closest bike share location
outputClosestFacilitiesName1 = "ClosestBike"
# in this demo, only one location will be selected,
# user can still change the number of near by bike share location as many as they want
Number_of_Facilities_to_Find=4

# Network analysis to find the closest bike share location
arcpy.FindClosestFacilities_na(incidents1, facilities1, measurement_units,
                               networkDataset, outputGeodatabase, outputRoutesName1,
                               outputDirectionsName1, outputClosestFacilitiesName1,
                               Number_of_Facilities_to_Find)

print 'Network Analysis for finding the closest bike share location finished'

# Set local variables
incidents = r'ClosestBike'
facilities = r'evacuationExit'
# routes results
outputRoutesName = "RoutestoExit"
# directions
outputDirectionsName = "DirectionstoExit"
# selected closest evacuation exit
outputClosestFacilitiesName = "ClosestExit"
# in this demo, only one location will be selected,
# user can still change the number of near by exits as many as they want
Number_of_Facilities_to_Find=1

# Network analysis to find Closest Exit
arcpy.FindClosestFacilities_na(incidents, facilities, measurement_units,
                               networkDataset, outputGeodatabase, outputRoutesName,
                               outputDirectionsName, outputClosestFacilitiesName,
                               Number_of_Facilities_to_Find)

print 'Network Analysis for finding the closest exit finished'

# Set local variables
inFeatures1 = "RoutestoBike"
inFeatures2 = "DirectionstoBike"
inFeatures3 = "ClosestBike"
inFeatures4 = "RoutestoExit"
inFeatures5 = "DirectionstoExit"
inFeatures6 = "ClosestExit"
outLocation = "C:\Users\/no281\PycharmProjects\Final\Final_Project"
outFeatureClass1 = "RoutestoBike"
outFeatureClass2 = "DirectionstoBike"
outFeatureClass3 = "ClosestBike"
outFeatureClass4 = "RoutestoExit"
outFeatureClass5 = "DirectionstoExit"
outFeatureClass6 = "ClosestExit"
# delimitedField = arcpy.AddFieldDelimiters(env.workspace, "NAME")
# expression = delimitedField + " = 'Post Office'"

# Execute FeatureClassToFeatureClass, export data from geodb to regular file system as shp file
# data in shp file format can be read and visualize
arcpy.FeatureClassToFeatureClass_conversion(inFeatures1, outLocation,
                                            outFeatureClass1)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures2, outLocation,
                                            outFeatureClass2)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures3, outLocation,
                                            outFeatureClass3)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures4, outLocation,
                                            outFeatureClass4)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures5, outLocation,
                                            outFeatureClass5)

arcpy.FeatureClassToFeatureClass_conversion(inFeatures6, outLocation,
                                            outFeatureClass6)

print 'Data exporting finished'
print 'Waiting for data visualization'
