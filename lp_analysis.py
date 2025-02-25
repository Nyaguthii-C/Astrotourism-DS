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
