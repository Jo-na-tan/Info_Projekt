import folium


m = folium.Map(location=(41, -73), zoom_start=10)
fg = folium.FeatureGroup(name="Weg").add_to(m)


#print(adj)

#exit(0)


    #folium.Marker([tmp[1], tmp[0]]).add_to(fg)


folium.Marker([41, -73], popup='My Home').add_to(m)
folium.LayerControl().add_to(m)

m.save("index.html")