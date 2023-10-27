import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from PIL import Image
import geopandas as gpd
import matplotlib.cm

# Page Configuration
st.set_page_config(page_title="Airbnb",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Creating Page
option = option_menu(menu_title=None,
                     options=["Home","Analysis","Map"],
                     icons=['house','graph-up','globe-central-south-asia'],
                     default_index=0,
                     orientation='horizontal',
                     styles={'backgroundColor':'#ead6f1',
                             'secondaryBackgroundColor':'#fffdfd',
                             'primaryColor':'#c385cb',
                             'textColor':'#0c0c0c'})
df = pd.read_csv("C:\Guvi_projects\Airbnb_collections\simplified_airbnb.csv")

# Home Menu
if option == "Home":
    col1,col2 = st.columns(2)
    with col1:
        st.image('Airbnb_logo.png', use_column_width='always')
    with col2:
        st.title('Travel Industry, Property Management and Tourism ')
        st.write('Airbnb.Inc is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences.'
                 'The company acts as a broker and charges a commission from each booking.'
                 'The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.'
                 'Airbnb is a shortened version of its original name, AirBedandBreakfast.com. ')

elif option == 'Analysis':
    with st.sidebar:
        countries = df['country'].unique()
        country = st.multiselect(label='select a country', options=countries)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        all = st.checkbox('All neighbourhoods')
    with col2:
        cities = df[df['country'].isin(country)]['host_neighbourhood'].unique()
        city = st.selectbox(label='select a neighbourhood', options=cities,disabled=all)
    with col3:
        type = st.selectbox(label="select a property",options=['property_type', 'room_type', 'bed_type'])
    with col4:
        measure = st.selectbox(label='select a measure',options=['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating'])
    with col5:
        metric = st.radio(label="Select One",options=['Sum','Avg'])
    if metric == 'Avg':
        a = df.groupby(['host_neighbourhood',type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee', 'review_scores_rating']].mean().reset_index()
    else:
        a = df.groupby(['host_neighbourhood', type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
    if not all:
        b = a[a['host_neighbourhood'] == city]
    else:
        if metric=='Avg':
            a = df.groupby(['country',type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee', 'review_scores_rating']].mean().reset_index()
        else:
            a = df.groupby(['country', type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
        b = a[a['country'].isin(country)]
    st.header(f"{metric} of {measure}")
    # with st.expander('View Dataframe'):
    #     st.write(b.style.background_gradient(cmap=matplotlib.cm.get_cmap('Reds')))

    try:
        b['text'] = b['country'] + '<br>' + b[measure].astype(str)
        fig = px.bar(b, x=type, y=measure, color='country', text='text')
    except:
        b['text'] = b['host_neighbourhood'] + '<br>' + b[measure].astype(str)
        fig = px.bar(b, x=type,y=measure,color=type,text='text')
    st.plotly_chart(fig,use_container_width=True)
    # donut chart
    fig = px.pie(b, names=type, values=measure, color=measure,hole=0.5)
    fig.update_traces(textposition='outside', textinfo='label+percent')
    st.plotly_chart(fig, use_container_width=True)
    # ['label', 'text', 'value', 'percent']

elif option == "Map":
    with st.sidebar:
        measure = st.selectbox(label='select a measure', options=['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price','cleaning_fee', 'review_scores_rating'])

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    merged_data = pd.merge(world, df, left_on='name', right_on='country', how='inner')
    
    a = merged_data.groupby('country')[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].mean().reset_index()
    b = merged_data.groupby('country')['iso_a3'].first()
    c = pd.merge(a,b,left_on='country', right_on='country', how='inner')
    fig = px.choropleth(c,
                        locations='iso_a3',
                        color=measure,
                        hover_name='country',
                        projection='natural earth', # 'natural earth','equirectangular', 'mercator', 'orthographic', 'azimuthal equal area'
                        color_continuous_scale='YlOrRd')

    fig.update_layout(title=f'Avg {measure}',
                        geo=dict(showcoastlines=True,coastlinecolor='Black',showland=True,landcolor='white')
                     )
    st.plotly_chart(fig, use_container_width=True)

    a = merged_data.groupby('country')[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
    b = merged_data.groupby('country')['iso_a3'].first()
    c = pd.merge(a, b, left_on='country', right_on='country', how='inner')
    fig = px.choropleth(c,locations='iso_a3',
                        color=measure,
                        hover_name='country',
                        projection='natural earth',# 'natural earth','equirectangular', 'mercator', 'orthographic', 'azimuthal equal area'
                        color_continuous_scale='YlOrRd')

    fig.update_layout(
            title=f'Total {measure}',
            geo=dict(
                showcoastlines=True,
                coastlinecolor='Black',
                showland=True,
                landcolor='white')
        )
    st.plotly_chart(fig, use_container_width=True)













 
 
 
 
 


 
 
 
 
 
 

 
 

 
 
 


