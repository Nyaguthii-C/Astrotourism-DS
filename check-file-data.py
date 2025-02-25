import json

# Load and inspect the GeoJSON structure
with open("kenya_counties.geojson") as f:
    geojson_data = json.load(f)

# Print the first feature's properties
print(geojson_data["features"][0]["properties"])

