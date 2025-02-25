import geopandas as gpd

# Load Kenya boundaries (counties)
kenya_shp_path = "kenya_shapefile/gadm41_KEN_1.shp"
kenya_gdf = gpd.read_file(kenya_shp_path)

# Inspect the file
print(kenya_gdf.head())

