import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import plotly.graph_objects as go
from supabase import create_client, Client
import json

@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

@st.cache_data(ttl=15)
def run_query():
    return supabase.table("kebisingan2").select("*").order("id_kebisingan", desc=True).limit(4).execute()

def convert_dict_to_df(data):
    df = pd.DataFrame.from_dict(data)
    return df
    
st.title("Real-Time Monitoring Kebisingan Dashboard")

st.sidebar.header('Dashboard Monitoring Kebisingan')
st.sidebar.subheader('Kebisingan Parameter')
option = st.sidebar.selectbox(
    'Silakan pilih menu:',
    ('Home', 'About')
)
if option == 'Home':
    placeholder = st.empty()
    while True:
        supabase = init_connection()
        rows = run_query()
        rows = rows.model_dump_json()
        rows = json.loads(rows)
        if len(rows['data']) == 4:
            with placeholder.container():
                df = convert_dict_to_df(rows['data']).sort_values(by=["id_kebisingan"])
                z = df.iloc[0:4, 1:5].values
                colorscale = [[0, 'darkviolet'], [0.5, 'yellowgreen'], [1, 'red']]
                fig = go.Figure(data=
                go.Contour(
                    z = z, 
                    contours = dict(
                        coloring ='heatmap',
                        showlabels = True,
                        labelfont = dict(
                            size = 10,
                            color = 'black',
                        )
                    ) , 
               colorscale = colorscale )
                               )
                for j in range(4):
                    for k in range(4):
                        fig.add_annotation(x=j, y=k, text=str(z[j,k]), showarrow=False, font_size=10, font_color='black')
                fig.update_layout(margin=dict(l=10, r=10, b=10, pad=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, theme="streamlit")
                fig_surface = go.Figure(data=[go.Surface(z=z, colorscale=colorscale)])
                fig_surface.update_layout(margin=dict(l=10, r=10, b=10, pad=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', width=750, height=750)
                st.plotly_chart(fig_surface, theme="streamlit")
        else:
            with placeholder.container():
                st.write("Not Enough Data!")
        time.sleep(1)
