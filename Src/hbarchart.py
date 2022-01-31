#
# This file contains the functions to create the horizontal bar chart viz
#


# External lib
import numpy as np
import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

# Internal lib
import preprocess_vsHBarChart

def get_h_barchart_hover_template():
    '''
    Cette fonction permet de retourner la structure
    du hover pour le sunburst.
    
    Retourne:
    Structure du hovertemplate.
    '''
    hover = '<b>%{y}</b>  <br>' + \
            '<b>%{x}</b> production(s)<br>'+ \
            '<extra></extra>'
    return hover


def create_h_barchart_dropdown_menu(h_barchart_df):
    # Create options
    options = h_barchart_df["nomComplet"].map(lambda n: {"label": n, "value": n})
    # Create menu
    ddm = dcc.Dropdown(
        id='hbarchart-dropdown-menu',
        options=options,
        value='Étienne Desrosiers',
    )

    return ddm


def sort_genres(data_df):
    if data_df['Genres'] == "n.d.":
        return -1
    return data_df['Producer']


def create_h_barchart_fig(producer, h_barchart_df, avg_df):
    
    # Set variables used for fig
    y_avg = avg_df['genre'].values
    x_avg = avg_df['moyenne'].values
    #y_producer = h_barchart_df[h_barchart_df['nomComplet']==producer]['genre'].values
    #x_producer = h_barchart_df[h_barchart_df['nomComplet']==producer]['nombreDeFilms'].values

    producer_data = h_barchart_df[h_barchart_df['nomComplet']==producer][['genre', 'nombreDeFilms']]
    y_producer = producer_data['genre'].values
    x_producer = producer_data['nombreDeFilms'].values

    data_df = avg_df[['genre', 'moyenne']].merge(producer_data, on='genre', how='outer')
    data_df = data_df.rename(columns={'genre': 'Genres', 'moyenne': 'Moyenne', 'nombreDeFilms': 'Producer'})
    data_df = data_df.fillna(0)
    #data_df = pd.DataFrame({'Genres' : y_avg, 'Moyenne': x_avg, 'Producer': x_producer})

    data_df = data_df.iloc[data_df.apply(sort_genres, axis=1).argsort()]
    data_df['Moyenne'] = data_df['Moyenne'].round(1)
    data_df['Genres'] = data_df['Genres'].replace(['Sf'], 'SF')

    # Instatiate new fig
    fig = go.Figure()
    
    # Add trace for average
    fig.add_trace(
        go.Bar(
            name="Moyenne",
            x=data_df['Moyenne'],
            y=data_df['Genres'],
            orientation='h',
            marker_color = '#9C1D00',
            hovertemplate=get_h_barchart_hover_template(),
            text='Moyenne',
        )
    )
    # Add trace for the producer
    fig.add_trace(
        go.Bar(
            name=producer, 
            x=data_df['Producer'],
            y=data_df['Genres'],
            orientation='h',
            marker_color = '#81B4E3',
            hovertemplate=get_h_barchart_hover_template(),
            text=[producer],
        )
    )

    # Compose title
    title_str = "Genres explorés par " + producer
    
    # Set layout
    fig.update_layout(
        title=title_str,
        title_x=0.45,
        font_family="Helvetica",
        font_color="#3B3838",
        barmode='group',
        xaxis_title="Nombre de films",
        yaxis_title="Genre",
        height=600,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')

    return fig


def create_h_barchart_graph(h_barchart_fig):
    h_barchart_graph = dcc.Graph(
        figure=h_barchart_fig, 
        id='h-barchart-graph',
        config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False,
        )
    )

    return h_barchart_graph


def create_h_barchart(h_barchart_graph, h_barchart_ddm):  # h_barchart_title
    
    h_barchart = html.Div(
        style={'width':'600px'}, # style is set in app.py
        children=[
            #h_barchart_title,
            h_barchart_ddm,
            h_barchart_graph,
        ]   
    )

    return h_barchart