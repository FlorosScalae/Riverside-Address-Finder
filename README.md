# Riverside-Address-Finder
A Python script used to find postcodes that lie near rivers, the user can specify the name of the river and the radius of the search area.

# How to use 
Before you can use this program you'll need 2 things 
1. The name of the river you're interested in
2. A .gml file containing data about watercourses in the location you're interested in. An example document can be found [here](https://www.data.gov.uk/dataset/dc29160b-b163-4c6e-8817-f313229bcc23/os-open-rivers)

The .gml file contains a large number of watercourses each broken down into things called <b>HydroNodes</b> these contain the coordinates of points along the water course. A water course can contain many HydroNodes and each HydroNode can contain multiple coordinates, this program will find all of the available HydroNodes and extract the coordinates so we can find nearby postcodes.

Once you've got your file and your river you'll want to find the name of your river in your dataset.![image](https://github.com/FlorosScalae/Riverside-Address-Finder/assets/135989973/bfbc64cf-4291-4473-a876-be0ec47dd94d)
Shown above is a section of the .gml file linked above, the name of a watercourse is found in the tag <b><river:watercourseName></b>, inbetween these tags is the name of a watercourse. In this instance the name is "Milldale Burn" so this is the name we'd use in our program. 

You'll likely find that your .gml file will be very large thus searching through it manually isn't practical, use CTRL + F to search within the file using a text editor of your choice for the name of your river.
Note: some water features have multiple names (example shown below), make sure you use the name in <b><river:watercourseName></b>, not the name in <b><river:watercourseNameAlternative></b>. So for the image below we would use "River Thurso" as opposed to "Mill Pool".
![image](https://github.com/FlorosScalae/Riverside-Address-Finder/assets/135989973/d2a2d864-06e0-4ec4-8d5b-00f1eddee033)

Now that you've found the name of your watercourse you'll need the coordinate system your .gml file uses, once again you can use CTRL + F but this time search for "EPSG", you're looking for the number that comes after the colons, so for the image below that's <b>27700</b>.
![image](https://github.com/FlorosScalae/Riverside-Address-Finder/assets/135989973/d33b1134-2de9-4b93-8b62-6050879eb49a)

All you need to do now is put this information into the program and run it, open the program and look for these lines of code:
![image](https://github.com/FlorosScalae/Riverside-Address-Finder/assets/135989973/b9aef857-032b-4da3-a511-953d48437c6b)
Where it says <b>riverName = "Afon Gwy"</b> you'll want to replace "Afon Gwy" with "name of your river" (you neeed to include the quotation marks).
Where it says <b>coordSystem = "EPSG:27700"</b> you'll want to replace "EPSG:27700" with the coordinate system your data uses, i.e. "yourCoordinateSystem"

The program will find the postcodes of places within a given radius of each set of coordinates obtained from the HydroNodes, you can control how big a radius to use by altering the line <b>search radius = 1500</b>, the number after the equals sign can be any integer less than or equal to 2000 (this represents the search radius in metres, thus the larger this number the further away from the river you can get postcodes).

Finally if you want to visualise the course of the river taken from the file you can change <b>saveDrawCoords = False</b> to <b>saveDrawCoords = True</b>, this will create an additional text file that you can copy the contents of and plot using [this website](https://mobisoftinfotech.com/tools/plot-multiple-points-on-map/).

All that's left is to place the .gml in the same file folder as the python script and run the program, if successful you should find a csv file containing all of your postcodes in the same folder.
Note: this program requires an internet connection to function as it makes requests to an external API, because of this it may take some time for the program to finish so don't expect it to finish instantly.
