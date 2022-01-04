import folium
import pandas as pd
map = folium.Map(location=[42.58339742062781, -106.80714664892],tiles="Stamen Terrain")


data = pd.read_csv("Volcanoes.txt")

html = """<h4>Volcano information:</h4>
<p>Name: %s</p>
<p>Height: %s m</p>
<p>Type: %s</p>
<p>Latitude: %s</p>
<p>Longitude: %s</p>

"""
names = list(data['NAME'])
lats = list(data['LAT'])
lons = list(data['LON'])
elevs = list(data['ELEV'])
types = list(data['TYPE'])

def color_producer(elev=0):
    if elev < 2000:
        return "green"
    elif elev < 3000:
        return "orange"
    else:
        return "red"    

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")


fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function= lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 50000000
else 'orange' if x['properties']['POP2005'] < 100000000 else 'red'
}))

for name,lat,lon,elev,type in zip(names,lats,lons,elevs,types):
    iframe = folium.IFrame(html=html % (str(name),str(elev),str(type),str(lat),str(lon)) , width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lat,lon],popup=folium.Popup(iframe),radius=6,color='grey',
                    fill_color=color_producer(elev),fill_opacity=0.7))





map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("index.html")
