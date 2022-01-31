#
# This file contains the functions to create the table viz
#


# External lib
import numpy as np
import pandas as pd
import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc

import plotly.graph_objects as go

# Internal lib
import preprocess_vsCommon as common


def query_data_for_table(table_df, genre, from_year, to_year, top_n):
    
    # Replace function to use with .apply()
    def replace_string(x):
        if x in top_n_languages:
            return x
        else:
                return 'autres'

    # Extract data corresponding to the right genre
    if genre == "All":
        temp_df = table_df.copy()
    else:
        query_str = "genre=='" + genre + "'"
        temp_df = table_df.query(query_str)
    
    # Extract data corresponding to the right years
    query_str = "anneeSortie>=" + str(from_year)
    temp_df = temp_df.query(query_str)
    query_str = "anneeSortie<=" + str(to_year)
    temp_df = temp_df.query(query_str)
    
    # Extract oldest movie from that period
    oldest_date = temp_df['anneeSortie'].min()
    query_str = "anneeSortie==" + str(oldest_date)
    oldest_df = temp_df.query(query_str)
    
    # Extract latest movie from that period
    latest_date = temp_df['anneeSortie'].max()
    query_str = "anneeSortie==" + str(latest_date)
    latest_df = temp_df.query(query_str)
    
    # Get count of movies for each language
    top_n_df = (temp_df
        .groupby('langue')
        .agg(nombreDeFilms=pd.NamedAgg(column='anneeSortie', aggfunc='count'))
        .reset_index()
        .sort_values(['nombreDeFilms'], ascending=[False])
    )
    
    # handles cases where there is more than n languages
    if len(top_n_df) > top_n:
        # create a list with top n languages
        top_n_languages = top_n_df.head(top_n)['langue'].tolist()

        # replace non top n languages by "autres"
        top_n_df['langue'] = top_n_df['langue'].apply(lambda x: replace_string(x))

        # aggregate to have top n + autres languages
        top_n_df = (top_n_df
            .groupby(['langue'])
            .agg(nombreDeFilms=pd.NamedAgg(column='nombreDeFilms', aggfunc='sum'))
            .reset_index()
            .sort_values(['nombreDeFilms'], ascending=[False])
        )
    # else: no need to do anything
    
    # get the percentage of each language
    n_films = top_n_df['nombreDeFilms'].sum()
    top_n_df['pourcentageDeFilms'] = (top_n_df['nombreDeFilms']
        .apply(lambda x: 100 * x / n_films)
    )
    
    top_n_df = common.round_decimals(df=top_n_df, n_decimals=2)
    
    return top_n_df, oldest_df, latest_df


def create_table_title(year_min_displayed, year_max_displayed, genre_displayed, top_n):
    if genre_displayed=="All":
        title_str = (
            'INFOS COMPLÉMENTAIRES SUR LES FILMS PRODUITS ENTRE LES ANNÉES ' + 
            str(year_min_displayed) + 
            ' ET ' + 
            str(year_max_displayed)
        )
    else: 
        title_str = (
            'INFOS COMPLÉMENTAIRES SUR LES FILMS "' + 
            genre_displayed + 
            '" PRODUITS ENTRE LES ANNÉES ' + 
            str(year_min_displayed) + 
            ' ET ' + 
            str(year_max_displayed)
        )

    title = html.P(
        id='table-title', 
        children=title_str,
        style={'font-family':'Helvetica','font-size':'15px','font-weight': 'bold', "text-align": "center", 'color' : '#581f8d'}
    )
    
    return title


def create_table_range_slider(year_min, year_max):   
    # Create list of years
    first_decade = 10 - (year_min%10) + year_min
    last_decade = year_max - (year_max%10)
    years = np.arange(start=first_decade, stop=last_decade+1, step=10)

    rs = dcc.RangeSlider(
        id='table-range-slider',
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


def create_table_slider(initial_value):
    
    # Create list of years
    max_top = 10
    top_n = np.arange(start=1, stop=max_top+1, step=1)

    slider = dcc.RangeSlider(
        id='table-slider',
        min=1,
        max=max_top,
        value=[initial_value],
        pushable=False,
        allowCross=False,
        dots=False,
        updatemode='mouseup',
        marks={str(i): str(i) for i in top_n},
    )    
    
    return slider


def create_table_fig(top_n_df, oldest_df, latest_df, top_n):

    # Create table_top_n_fig
    table_top_n_fig = go.Figure(
        data=[
            go.Table(
                columnorder = [1,2,3],
                columnwidth = [100,100,100],
                header_values=["<b>Langue</b>", "<b>Nombre de films</b>", "<b>Proportion</b>"],
                header_fill_color='#81B4E3',
                header_align='center',
                cells_values=[top_n_df.langue, top_n_df.nombreDeFilms, top_n_df.pourcentageDeFilms.astype(str) + " %"],
                cells_fill_color='#E5ECF6',
                cells_align='left',
            )
        ]
    )
    
    table_top_n_fig.update_layout(
        title= 'TOP ' + str(top_n) + ': Langues des productions',
        title_x=0.5,
        font_family="Helvetica",
        font_color="#3B3838",
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=10,r=10)
    )
    # Filter n.d.
    #latest_df = latest_df[~(latest_df['langue'].isin([None, "n.d.", np.nan]))].head()

    # Create table_latest_fig 
    table_latest_fig = go.Figure(
        data=[
            go.Table(
                columnorder = [1,2,3],
                columnwidth = [200,50,60],
                header_values=["<b>Titre</b>", "<b>Année</b>", "<b>Langue</B>"],
                header_fill_color='#81B4E3',
                header_align='center',
                cells_values=[latest_df.titreOriginal, latest_df.anneeSortie, latest_df.langue],
                cells_fill_color='#E5ECF6',
                cells_align='left',
            )
        ]
    )

    table_latest_fig.update_layout(
        title="Les plus récentes oeuvres de la période",
        title_x=0.5,
        font_family="Helvetica",
        font_color="#3B3838",
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=10,r=10)
    )
    
    # Filter n.d.
    # oldest_df = oldest_df[~(oldest_df['langue'].isin([None, "n.d.", np.nan]))].head()
    
    # Create table_oldest_fig
    table_oldest_fig = go.Figure(
        data=[
            go.Table(
                columnorder = [1,2,3],
                columnwidth = [200,50,60],
                header_values=["<b>Titre</b>", "<b>Année</b>", "<b>Langue</B>"],
                header_fill_color='#81B4E3',
                header_align='center',
                cells_values=[oldest_df.titreOriginal, oldest_df.anneeSortie, oldest_df.langue],
                cells_fill_color='#E5ECF6',
                cells_align='left',
            )
        ]
    )

    oldest_df.anneeSortie
    table_oldest_fig.update_layout(
        title="Les plus anciennes oeuvres de la période",
        title_x=0.5,
        font_family="Helvetica",
        font_color="#3B3838",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10,r=10)
    )

    return table_top_n_fig, table_latest_fig, table_oldest_fig


def create_table_top_n_graph(table_top_n_fig):
    table_top_n_graph = dcc.Graph(
        figure=table_top_n_fig, 
        id='table-top-n-graph',
        config=dict(
            showTips=False,
            showAxisDragHandles=False,
            displayModeBar=False
        )
    )

    return table_top_n_graph


def create_table_latest_graph(table_latest_fig):
    table_latest_graph = dcc.Graph(
        figure=table_latest_fig, 
        id='table-latest-graph',
        config=dict(
            showTips=False,
            showAxisDragHandles=False,
            displayModeBar=False
        )
    )

    return table_latest_graph


def create_table_oldest_graph(table_oldest_fig):
    table_oldest_graph = dcc.Graph(
        figure=table_oldest_fig, 
        id='table-oldest-graph',
        config=dict(
            showTips=False,
            showAxisDragHandles=False,
            displayModeBar=False
        )
    )

    return table_oldest_graph



