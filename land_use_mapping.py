# Below is the first truly useful thing I ever wrote in Python. This script automates the process of generating
# a series of maps for land use review, designed to work with an .mxd file and an ESRI script tool.
# I had no idea what I was doing, but it worked!

# Tool authored by Dusty Pilkington, May 2017
# MSc, Central Washington University
# Cultural and Environmental Resource Management

# If have questions, please contact me at
# pilkingtongeospatial@gmail.com, or by telephone at 801-920-3638


import arcpy

arcpy.env.overwriteOutput = True
mxd = arcpy.mapping.MapDocument("G:\Dusty's_Work\MXDs\MappingArcpyNew.mxd")  # point ArcGIS to mapdocument to use
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # define the data frame to use
project_parcel = arcpy.GetParameterAsText(0)  # project layerfile to map
project_folder = arcpy.GetParameterAsText(1)#  Folder to place maps
file_number = arcpy.GetParameterAsText(2)  # File number for project
user_scale = arcpy.GetParameterAsText(3)  # Scale to map close up to project shapefile
project_folder_GIS = arcpy.GetParameterAsText(4)  #GIS folder to place shapefiles and excel spreadsheet
add_string = " Map "


# Define variables referencing layer files
# Import input shapefile and symbology (should have already copied from PROJECTS geodatabase to project folder)
addLayer = arcpy.mapping.Layer(project_parcel)
arcpy.mapping.AddLayer(df, addLayer, "TOP")
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

# Define variables to add and remove layers

current_lyrfile =  arcpy.mapping.ListLayers(mxd)[0]
Tax_Parcelslyr = arcpy.mapping.ListLayers(mxd)[1]
All_Roadslyr =  arcpy.mapping.ListLayers(mxd)[2]
BPA_Right_of_Waylyr = arcpy.mapping.ListLayers(mxd)[3]
Coal_Mine_Shaft_Boundarieslyr = arcpy.mapping.ListLayers(mxd)[4]
Wetlandsyr = arcpy.mapping.ListLayers(mxd)[5]
Streamslyr = arcpy.mapping.ListLayers(mxd)[6]
Floodplainlyr = arcpy.mapping.ListLayers(mxd)[7]
Floodwaylyr = arcpy.mapping.ListLayers(mxd)[8]
Fire_Districtslyr = arcpy.mapping.ListLayers(mxd)[9]
Irrigation_Districtslyr = arcpy.mapping.ListLayers(mxd)[10]
Landslideslyr = arcpy.mapping.ListLayers(mxd)[11]
Land_Uselyr= arcpy.mapping.ListLayers(mxd)[12]
School_Districtslyr = arcpy.mapping.ListLayers(mxd)[13]
Seismic_Categorylyr = arcpy.mapping.ListLayers(mxd)[14]
Urban_Growth_Area = arcpy.mapping.ListLayers(mxd)[15]
Zoninglyr = arcpy.mapping.ListLayers(mxd)[16]
Shorelineslyr = arcpy.mapping.ListLayers(mxd)[17]
Hazardouslyr = arcpy.mapping.ListLayers(mxd)[18]
PHSlyr = arcpy.mapping.ListLayers(mxd)[19]
Land_Projectslyr = arcpy.mapping.ListLayers(mxd)[20]
Aeriallyr = arcpy.mapping.ListLayers(mxd)[40]
CMZlyrT1lyr = arcpy.mapping.ListLayers(mxd)[47]
CMZlyrT2lyr = arcpy.mapping.ListLayers(mxd)[48]
Installationslyr = arcpy.mapping.ListLayers(mxd)[49]
SUAslyr = arcpy.mapping.ListLayers(mxd)[50]
MTRslyr = arcpy.mapping.ListLayers(mxd)[51]

#define variables to get to proper extent of project file

current_object = arcpy.mapping.Layer(project_parcel)
ext = current_lyrfile.getExtent(current_object)
df.extent = ext
df.scale = 10000
for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.text == "File Number":
        elm.text = file_number
arcpy.RefreshTOC()
arcpy.RefreshActiveView()


#define map export function
def mapfunction(maptype):
    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text != file_number:
            elm.text = maptype
    Extension = ".pdf"
    output_location = project_folder + "\\" + file_number + add_string + maptype + Extension
    arcpy.mapping.ExportToPDF(mxd, output_location)

#define the function to test whether certain features intersect the project. If the project lyrfile intersects the
# feature, export a map

def testfunction(list,maptypetest):
    counter = 0
    for l in list:
        maptyperep = maptypetest.replace(" ", "_")
        intersect = arcpy.Intersect_analysis([current_lyrfile,l], "in_memory" + "//" + maptyperep)
        result = arcpy.GetCount_management(intersect)
        count = int(result.getOutput(0))
        if count > 0:
            counter += 1
    if counter > 0:
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        mapfunction(maptypetest)

    arcpy.Delete_management("in_memory" + maptyperep)

All_Roadslyr.visible = True # Add layers for first map
Tax_Parcelslyr.visible = True
Tax_Parcelslyr.showLabels = True
Urban_Growth_Area.visible = True
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
mapfunction("Vicinity")  #Call mapfunciton to export map in PDF format

df.scale = user_scale  # center map layout at user defined scale on project layerfile
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

#Repeat process to create series of project maps

Wetlandsyr.visible = True
Streamslyr.visible = True
Floodplainlyr.visible = True
Floodwaylyr.visible = True
Urban_Growth_Area.visible = False
BPA_Right_of_Waylyr.visible = True
Tax_Parcelslyr.showLabels = False
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

Criticallist = [Wetlandsyr,Streamslyr,Floodplainlyr,Floodplainlyr]
testfunction(Criticallist,"CriticalAreas") # Call Testfunction to check if the project parcel intersects critical areas
# If true, export map

Wetlandsyr.visible = False
Streamslyr.visible = False
Floodplainlyr.visible = False
Floodwaylyr.visible = False
Urban_Growth_Area.visible = False
BPA_Right_of_Waylyr.visible = False
School_Districtslyr.visible = True
Fire_Districtslyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("School and Fire Districts")

School_Districtslyr.visible = False
Fire_Districtslyr.visible = False
Irrigation_Districtslyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
districtslist = [Irrigation_Districtslyr]
testfunction(districtslist,"Irrigation Districts")

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
Irrigation_Districtslyr.visible = False
Land_Uselyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Comprehensive Plan Land Use")

Land_Uselyr.visible = False
Seismic_Categorylyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Seismic Category")

UGAlist = [Urban_Growth_Area]
Seismic_Categorylyr.visible = False
Urban_Growth_Area.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
testfunction(UGAlist,"Urban Growth Area")

Urban_Growth_Area.visible = False
Zoninglyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Zoning")

Shorelineslyr.visible = True
Zoninglyr.visible = False
Shorelineslist = [Shorelineslyr]
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
testfunction(Shorelineslist,"Shorelines")

Shorelineslyr.visible = False
Coal_Mine_Shaft_Boundarieslyr.visible = True
Landslideslyr.visible = True
Coal_land_list = [Coal_Mine_Shaft_Boundarieslyr,Landslideslyr]
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
testfunction(Coal_land_list,"Coal Mines and Landslides")

Coal_Mine_Shaft_Boundarieslyr.visible = False

Landslideslyr.visible = False
Hazardouslyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Hazardous Slopes")

Hazardouslyr.visible = False

PHSlyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
PHSlist = [PHSlyr]
testfunction(PHSlist,"Priority Habitat Species")

PHSlyr.visible = False
Land_Projectslyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Land Use Projects")

Land_Projectslyr.visible = False
Aeriallyr.visible = True
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapfunction("Aerial View")

Aeriallyr.visible = False
CMZlyrT1lyr.visible = True
CMZlyrT2lyr.visible = True
CMZList = [CMZlyrT1lyr,CMZlyrT2lyr]
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
testfunction(CMZList,"Channel Migration Zones")