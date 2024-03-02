import backend  
import streamlit as st
from streamlit_folium import st_folium


@st.cache_data
def load_data(start, end):
    return backend.main(start, end)

st.set_page_config(layout="wide")

if 'start' not in st.session_state:
    st.session_state.start = [0, 0]

if 'end' not in st.session_state:
    st.session_state.end = [0, 0]

if 'center' not in st.session_state:
    st.session_state.center = (41, -73)

if 'zoom' not in st.session_state:
    st.session_state.zoom = 8


daten = load_data(st.session_state.start, st.session_state.end)




st.title("Informatik OOP Projekt") 

c1, c2 = st.columns([2,1])

with c1:
    st_data = st_folium(daten[0], width=1000, center=st.session_state.center, zoom=st.session_state.zoom, returned_objects=["all_drawings", "zoom", "center"])

with c2:
    if st.button("Weg berechnen"):
        if st_data.get("all_drawings")==None or len(st_data.get("all_drawings"))<=1:
            st.write("Bitte wählen Sie erst zwei Punkte auf der Karte")
        else:
            st.session_state.start=st_data.get("all_drawings")[0].get("geometry").get("coordinates")
            st.session_state.end=st_data.get("all_drawings")[1].get("geometry").get("coordinates")
            st.session_state.center=st_data.get("center")
            st.session_state.zoom=st_data.get("zoom")

            st.rerun()

    st.write("Startkoordinaten:", st.session_state.start[1], st.session_state.start[0])
    st.write("Zielkoordinaten:", st.session_state.end[1], st.session_state.end[0])

    st.write("kürzeste Länge:", round(daten[1]/16035, 1), "Meilen")
    st.write("geringste Zeit:", round(daten[2]/21972, 1), "Minuten")






#st.write(st_data)
