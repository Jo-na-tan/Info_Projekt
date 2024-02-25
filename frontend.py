import backend  
import folium
import streamlit as st
from streamlit_folium import st_folium



@st.cache_data
def load_data(start, end):
    return backend.main(start, end)



#st.set_page_config(layout="wide")

st.title("Info Projekt") 

start = st.number_input('Start', value=1)
end = st.number_input('Ziel', value=1)



daten = load_data(start, end)

st_data = st_folium(daten[0], width=700)


st.write("Start", st_data.get("last_clicked").get("lat"), st_data.get("last_clicked").get("lng"))
if st.button("Startpunkt wählen"):
    start=[st_data.get("last_clicked").get("lat"), st_data.get("last_clicked").get("lng")]

    st.write("End", st_data.get("last_clicked").get("lat"), st_data.get("last_clicked").get("lng"))
    if st.button("Endpunkt wählen"):
        end=[st_data.get("last_clicked").get("lat"), st_data.get("last_clicked").get("lng")]

st.write(start)

st.markdown(daten[1])

st.write(st_data)
st.write(type(st_data))