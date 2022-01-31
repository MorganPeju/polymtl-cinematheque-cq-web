#
# This file contains the functions to create the treemap viz
#


# External lib
import json
import numpy as np
import pandas as pd
import datetime


# Internal lib
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

def get_treemap_hover_template():

    hover = '<b>%{label}</b>  <br><br>' + \
            '<b>%{value}</b> productions <br>'+ \
            '<extra></extra>'
    return hover

def clean_country_column_for_treemap(df): 

    def extract_country(x):
        temp = x.split(':')
        if len(temp)==2:
            return temp[0][:-1]
        else:
            return x

    # Explicit copy
    temp_df = df.copy()

    # Set missing values
    temp_df['pays'] = temp_df['pays'].fillna("n.d.")

    # Extract country 
    temp_df['pays'] = temp_df['pays'].apply(lambda x: extract_country(x))

    return temp_df

def create_treemap_dropdown_menu(genres):
    # Create options
    options=[{'label': "All", 'value': "All"}]
    for genre in genres:
        option = {'label': genre, 'value': genre}
        options.append(option)

    # Create menu
    ddm = dcc.Dropdown(
            id='treemap-dropdown-menu',
            options=options,
            value='All',
        )
    
    return ddm


def create_treemap_title(year_min_displayed, year_max_displayed, genre_displayed):
    
    if genre_displayed=="All":
        title_str = (
            'Nombre de films de tous genres produits entre les années ' + 
            str(year_min_displayed) + 
            ' et ' + 
            str(year_max_displayed)
        )
    else: 
        title_str = (
            'Nombre de films du genre ' + 
            genre_displayed + 
            ' produit entre les années ' + 
            str(year_min_displayed) + 
            ' et ' + 
            str(year_max_displayed)
        )

    title = html.Header(
        id='treemap-title', 
        children=title_str
    )
    
    return title


def create_treemap_range_slider(year_min, year_max):
    
    # Create list of years
    first_decade = 10 - (year_min%10) + year_min
    last_decade = year_max - (year_max%10)
    years = np.arange(start=first_decade, stop=last_decade+1, step=10)

    rs = dcc.RangeSlider(
        id='treemap-range-slider',
        min=year_min,
        max=year_max,
        value=[year_min, year_max],
        pushable=False,
        allowCross=True,
        dots=False,
        updatemode='mouseup',
        marks={str(year): str(year) for year in years},
    )    
    
    return rs


def query_data_for_treemap(df, genre, from_year, to_year):
    
    # Extract data corresponding to the right genre
    if genre == "All":
        temp_df = df
    else:
        query_str = "genre=='" + genre + "'"
        temp_df = df.query(query_str)
    
    # Extract data corresponding to the right years
    query_str = "anneeSortie>=" + str(from_year)
    temp_df = temp_df.query(query_str)
    query_str = "anneeSortie<=" + str(to_year)
    temp_df = temp_df.query(query_str)
        
    # Aggregate agnostic to years
    temp_df = (temp_df
        .groupby(['planete', 'continent', 'pays'])
        .agg(nombreDeFilms=pd.NamedAgg(column='genre', aggfunc='count'))
        .reset_index()
    )
    return temp_df


def create_treemap_fig(df, year_min, year_max):
    # Get data
    temp_df = query_data_for_treemap(
        df=df, 
        genre='All', 
        from_year=year_min, 
        to_year=year_max
    )
    
    # Create a figure with px
    fig = px.treemap(
        temp_df, 
        path=['planete', 'continent', 'pays'], 
        values='nombreDeFilms',
        hover_name="pays",
        color_discrete_sequence=px.colors.sequential.BuPu,
    )

    fig.update_traces(
        hovertemplate=get_treemap_hover_template(),
        marker_line=dict(
            color='grey'
        )
    )
        
    fig.update_layout(
        #height=500,
        margin=dict(l=0,r=0,b=20,t=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_treemap_graph(treemap_fig):
    treemap_graph = dcc.Graph(
        figure=treemap_fig,
        id='treemap-graph',
        config=dict(
            showTips=False,
            showAxisDragHandles=False,
            displayModeBar=False
        )
    )

    return treemap_graph


def create_treemap(treemap_title, treemap_rs, treemap_ddm, treemap_graph):
    
    treemap = html.Div(
        style={'width' : '600px'}, 
        children=[
            treemap_title,
            treemap_ddm,
            treemap_graph,
            treemap_rs
        ]
    )
    return treemap