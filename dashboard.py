import streamlit as st
import pandas as pd
import pydeck as pdk

#githubtest

df = pd.read_excel('data.xlsx')
#max_value = df['Valor']
#max_value = maior.max(axis = 0)
#df['scale'] = df['value']/max_value*255
#df['scale'] = df['scale'].round(decimals = 0)
df['place1'] = df['place']
df = df.rename(columns={'place1':'index'}).set_index('index')
st.write("### Filter")
local=st.multiselect(
    "Pick a place", list(df.index),["Brasilia","Porto Velho"]
)
if not local:
    st.error("Select a place")
else:
    data = df.loc[local]
    data1 = data
    data1 = data1.drop(['in_lat', 'in_long','out_lat','out_long','place'], axis = 1)
    data1 = data1.style.set_properties(**{
        'background-color' : 'indianred',
        #'font-size': '11pt',
        }
    )
    st.write("### Data")
    st.dataframe(data1)
    #st.table(data1)

slayer = pdk.Layer(
    'ScatterplotLayer',
    data = data,
    get_position = ["out_long","out_lat"],
    get_color = [200, 30, 0, 160],
    get_line_color = [0, 0, 0],
    get_radius = "value*1000",
    pickable = True,
    onClick = True,
    filled = True,
    line_width_min_pixels = 10,
    opacity = 2,

)

layer = pdk.Layer(
    "ArcLayer",
    data = data,
    get_source_position = ["in_long","in_lat"],
    get_target_position = ["out_long","out_lat"],
    get_source_color = [200, 30, 0, 160],
    get_target_color = [200, 30, 0, 160],
    auto_highlight = True,
    width_scale = 0.1,
    get_width = "value",
    width_min_pixels = 3,
    width_max_pixels = 300,
    pickable = True,
    onClick = True,
    )
initial_view = pdk.ViewState(
    latitude=-20.476108,
    longitude=-54.612962,
    zoom = 4,
    pitch = 50
)
tooltip_text = {
    "html":
        "<b>Value:</b> {value} units <br/>"
        "<b>Place:</b> {place} <br/>",
    "style":{
        "backgroundColor": "indianred",
        "color" : "black",
    }
}
st.write('### Map')
st.pydeck_chart(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = initial_view,
    #api_keys = api_token,
    map_provider = 'mapbox',
    layers = [layer, slayer],
    tooltip = tooltip_text,
    )
)
st.button("Update Data")