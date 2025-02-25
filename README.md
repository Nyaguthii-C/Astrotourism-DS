 # Astronomy Tourism Project

Loading [light pollution data](https://dataservices.gfz-potsdam.de/contact/showshort.php?id=escidoc:1541893&contactform) and [cloud cover data](https://www.meteoblue.com/en/weather/historyclimate/climatemodelled/sossusvlei_namibia_3353011) and making choropleth maps of regions in kenya using shapefiles like [this](https://plotly.com/python/choropleth-maps/)

## Objective
Learn how to extract data light pollution and cloud cover data with Data Science Tools to analyze possible suitable AstroTourism locations in Kenya



## Initial Setting Up(Ubuntu 20.04 python environment) - Visualizing LP DaTa
- Make or navigate into a directory.  
```
mkdir Astronomy-Tourism-Project
```
- Create a virtual environment  

```
python3 -m venv venv
```
- Activate the Virtual Environment  
```
source venv/bin/activate
```

- Install required Python libraries
```
pip install geopandas rasterio rasterstats plotly pandas

```
- Download Kenya Shapefile from GADM

```
wget https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_KEN_shp.zip
unzip gadm41_KEN_shp.zip -d kenya_shapefile

```

- Load Kenya Shapefile, extract Light Pollution Data from the .tif File(assuming it was downloaded earlier from with the light pollution data), convet the Data for Plotly and create a Choropleth Map with Plotly. The script below does that and outputs the map into the output.html file as well.   
- **Vim lp_analysis.py**

```
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import plotly.express as px
import pandas as pd
import json
import webbrowser
import plotly.io as pio


# -------------------------------
# 1. Load Kenya Shapefile
# -------------------------------
kenya_shp_path = "kenya_shapefile/gadm41_KEN_1.shp"
kenya_gdf = gpd.read_file(kenya_shp_path)

# -------------------------------
# 2. Read Light Pollution Data from TIF
# -------------------------------
tif_path = "./World_Atlas_2015-data/World_Atlas_2015.tif"

# Compute mean light pollution per county
stats = zonal_stats(kenya_shp_path, tif_path, stats=["mean"])

# Add extracted LP values to the GeoDataFrame
kenya_gdf["light_pollution"] = [s["mean"] for s in stats]

# -------------------------------
# 3. Convert to GeoJSON for Plotly
# -------------------------------
kenya_gdf = kenya_gdf.to_crs(epsg=4326)  # Convert to Lat/Lon projection
kenya_geojson = json.loads(kenya_gdf.to_json())  # Convert to proper JSON format

# Debugging output
print("GeoJSON keys:", kenya_geojson.keys())  # Should print: dict_keys(['type', 'features'])
print("Sample feature properties:", kenya_geojson["features"][0]["properties"])  # Should show properties

# -------------------------------
# 4. Plot Choropleth Map with Plotly
# -------------------------------
df = pd.DataFrame(kenya_gdf)

fig = px.choropleth(
    df,
    geojson=json.loads(json.dumps(kenya_geojson)),  # Ensures proper JSON
    locations="NAME_1",  # Use county names
    featureidkey="properties.NAME_1",  # match GeoJSON properties
    color="light_pollution",
    # color_continuous_scale="YlOrRd",
    color_continuous_scale="Viridis",
    # range_color=(0, 1),
    title="Light Pollution Levels in Kenya",
)

# Adjust map settings
fig.update_geos(
    fitbounds="locations",
    visible=False,
    projection_type="mercator"  # Proper projection
)

# Show or Save Output
fig.write_html("output_map.html")  # Save as HTML
# webbrowser.open("output_map.html")  # Auto-open in browser

# Set browser-based rendering
pio.renderers.default = "browser"

# Now, show the figure
fig.show()

```