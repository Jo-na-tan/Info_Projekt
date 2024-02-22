import backendFL
import folium
import streamlit as st
from streamlit_folium import st_folium



@st.cache_data
def load_data(start, end):
    return backendFL.main(start, end)



#st.set_page_config(layout="wide")

st.title("Info Projekt") 

start = st.number_input('Start', value=1)
end = st.number_input('Ziel', value=1)

daten = load_data(start, end)

st_data = st_folium(daten[0], width=700)

st.markdown(daten[1])