import folium
import pandas

# Opening the Volcanoes.txt file and storing it in the variable data
data = pandas.read_csv("Volcanoes.txt")

# Converting the values in LAT and LON columns into a list and storing it in the variables
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

html = """<h4>Volcano information:</h4>
Height: %s m
"""

# The function will have some conditions for each of which it returns different color based on the number of elevations
def marker_color(elevations):
    if elevations < 1000:
        return "green"
    elif 1000 <= elevations < 3000:
        return "orange"
    else:
        return "red"

# The code below will locate to the location specified
# It will have a zoom level of 6 at the beginning
# The background style will be "Stamen Terrain"
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

# The for loop will create as many markers as locations specified in the list
for lt, ln, el in zip(lat, lon, elev):

    # This will style the popup window
    iframe = folium.IFrame(html=html % str(el), width=200, height=100)

    # The code below will add a marker(a pin) to the location specified
    # The marker will have a green color
    # On clicking the marker, the popup will appear saying "Hi I am a marker"
    # The icon property (color of the marker) will change as the number of elevations varies
    fgv.add_child(folium.Marker(location=[lt, ln], radius=6, popup=folium.Popup(iframe, parse_html=True), icon=folium.Icon(color=marker_color(el))))

    # Code to covert the marker into a circle
    # fg.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe, parse_html=True), fill_color = marker_color(el), color = 'grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

# The code below will add polygons (borders) to the map with the help of world.json file
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8 sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000
else 'orange' if 1000000 <= x['properties']['POP2005'] < 2000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")