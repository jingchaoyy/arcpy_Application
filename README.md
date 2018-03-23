# arcpy_NetworkAnalysis
Network analysis from arcpy to identify closest facilities from incidents
1.	Datasets (all from opendata.dc.gov, and with GCS_WGS_1984):
a.	Regional Evacuation Route
b.	Capital Bike Share Locations
c.	DC Boundary
d.	Emergency Walkout Route
e.	Street Centerlines
2.	Data Preprocessing Tool
a.	Setting up arcpy environment
b.	arcpy.Clip_analysis for cutting Capital Bike Share Locations datasets and Regional Evacuation Route
c.	Hand draw Evacuation Exits and User locations
d.	Build network dataset from Street Centerlines, link for the processes: (http://desktop.arcgis.com/en/arcmap/latest/extensions/network-analyst/exercise-1-creating-a-network-dataset.htm)
3.	Network Analysis Tool
a.	arcpy.FindClosestFacilities_na, here is a link from Esri for the description: (http://desktop.arcgis.com/en/arcmap/10.3/tools/network-analyst-toolbox/find-closest-facilities.htm)
i.	Applied this function twice: One for calculating the closest bike share location based on the user location; one for calculating the closest evacuation exit from the selected bike share location based on the first application of this function. Output will provide users basic information after each step been executed.
ii.	Users of this code can decide whether to find one closest facilities or more
iii.	Users can also decide if they want to skip looking for bike share location and find the closest evacuation exit(s) riding their own bike
iv.	This function provide fastest route to the aimed exit based on the travel distance within our network dataset.
b.	arcpy.FeatureClassToFeatureClass_conversion, used to export routes, directions, and closest facilities find from a geodatabase to regular file directory as shapefiles (for visualization we need .shp and .shx file)
4.	Visualization Tool
a.	Read shape files, includes
i.	Datasets from opendata.dc.gov
ii.	Datasets from data preprocessing
iii.	Closest bike location
iv.	Routes from user locations to the closest bike locations
v.	Closest evacuation exit
vi.	Routes from selected bike locations to the closest evacuation exits
vii.	Routes from all bike share location to their closest exit
viii.	Routes from user locations to their closest evacuation exits
b.	Determine bounding box 
c.	Create canvas
d.	Determine ratio according to the canvas size
e.	Three options for drawing on canvas (Tkinter):
i.	Fastest route out of DC from user location to a bike share location first: 
require dataset i, ii, iii, iv, v, vi
 <img src="data/Option1.jpg" />
ii.	Route out of DC from Any Location: 
require dataset i, ii, vii
 
iii.	Fastest routes out of DC from all bike share locations:
require dataset i, ii, viii
 

5.	Reuse the program
a.	arcpy.Delete_management, used to delete all the datasets generated from network analysis, either inside or outside the geodatabase 
b.	Run the Network Analysis Tool again to reproduce routes accordingly, and use Visualization Tool for the visualization 
