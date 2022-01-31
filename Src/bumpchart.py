#
# This file contains the functions to create the bumpchart viz
#


# External lib
import json
import numpy as np
import pandas as pd
import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go

# Internal lib
import preprocess_vsBumpChart


def create_bumpchart_dropdown_menu(genres):
    # Create options
    options=[{'label': "All", 'value': "All"}]
    for genre in genres:
        option = {'label': genre, 'value': genre}
        options.append(option)

    # Create menu
    ddm = dcc.Dropdown(
            id='bumpchart-dropdown-menu',
            options=options,
            value='All',
        )
    
    return ddm


def create_bumpchart_fig(bumpchart_df):

    # Create raw fig
    fig = go.Figure()

    # Set lists
    x_data = bumpchart_df["decennie"]
    y_data = bumpchart_df["rang"]
    counts = bumpchart_df['compte']
    genreCat = bumpchart_df['genre']
    genres = bumpchart_df['genre'].unique()
    
    # Set theme
    temporary_theme = px.colors.sequential.dense[2:] + list(reversed(px.colors.sequential.RdPu))[:-2]

    # Add traces
    for idx, genre in enumerate(genres):
        fig.add_trace(
            go.Scatter(
                x=x_data[genreCat==str(genre)],
                y=y_data[genreCat==str(genre)],
                name=genre,
                mode='lines+markers',
                text=bumpchart_df['compte'][genreCat==str(genre)],
                hovertemplate="<b>%{text} production(s)</b>",
                marker_color= temporary_theme[idx],
                yaxis="y",
            )
        )
    
    x_bg = np.repeat([*range(1910, 2019, 10), 2019],max(y_data))
    y_bg = [*range(1,max(y_data)+1,1)]*max(y_data)
    fig.add_trace(go.Scatter(
        x=x_bg,
        y=y_bg,
        mode='markers',
        marker_symbol='square',
        marker_color="lightgrey",
        yaxis="y2",
        hoverinfo='none',
        ))

    x_data = bumpchart_df["decennie"]
    y_data = bumpchart_df["rang"]
    y_genre = bumpchart_df["genre"]
    
    rank_range_descending = [max(bumpchart_df["rang"])+1, 0]
    rank_range_ascending = [*range(min(y_data),max(y_data)+1,1)]

    fig = go.Figure(fig)
        
    fig.update_layout(
        hovermode='x',
        margin=dict(t=25),
        dragmode=False,
        hoverlabel=dict(
            bgcolor= 'white',
        ),
        xaxis=dict(
            title="Année de production",
            tickmode = 'array',
            tickvals= x_data,
            ticktext= x_data,
            tickangle = -45,
            fixedrange=True,
            scaleratio = 4,
        ),
        yaxis=dict(
            range=rank_range_descending,
            tickmode="array",
            tickvals= y_data[x_data == max(x_data)],
            ticktext= y_genre[x_data == max(x_data)],
            showgrid= False,
            anchor="x",
            overlaying="y2",
            side="right",
            scaleratio = 4,
            position=0.15
            ),
        yaxis2=dict(
            title="Rang",
            range=rank_range_descending,
            tickmode="array",
            tickvals= rank_range_ascending,
            ticktext= rank_range_ascending,
            anchor="x",
            side="left",
            constrain='domain',
            position=0.15
            ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
    )
    # Change grid color and axis colors
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='grey')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    
    return fig


def create_bumpchart_graph(bumpchart_fig):
    bumpchart_graph = dcc.Graph(
        figure=bumpchart_fig, 
        id='bumpchart-graph',
        config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False,
        ),
    )

    return bumpchart_graph


def create_bumpchart(bumpchart_ddm, bumpchart_graph):  # bumpchart_title
    
    bumpchart = html.Div(
        style={'width':'600px'}, 
        children=[
            #bumpchart_title,
            bumpchart_ddm,
            bumpchart_graph,
        ]   
    )

    return bumpchart