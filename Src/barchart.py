#
# This file contains the functions to create the barchart viz
#


# External lib
import numpy as np
import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc

import plotly.graph_objects as go

# Internal lib
# none


def compute_plot_marker_height(barchart_df):
    '''
    Compute the height in the scatter plot (histogram). The height
    does not encode a data per-say but is used to distinguish multiple
    persons who have the same number of distinctions.
    '''

    # Extract min max
    min_count = barchart_df.min()
    max_count = barchart_df.max()

    # Compute the height of each person in the scatter plot (custom histogram)
    temp_df = pd.Series(np.zeros((barchart_df.size, )), index = barchart_df.index)

    for c in range(min_count, max_count + 1):
        # Get positions of people with "c" distinctions
        bool_idx = barchart_df == c
        if not bool_idx.sum() == 0:
            temp_df[bool_idx] = np.arange(bool_idx.sum())

    return temp_df


def create_barchart_fig(barchart_df):
    '''
    Return the scatter plot (custom histogram) that represents the distribution of
    distinctions.
    '''
    
    # Compute height_df
    height_df = compute_plot_marker_height(barchart_df) 

    # Extract min max#
    min_count = barchart_df.min()
    max_count = barchart_df.max()
    max_height = height_df.max()

    # Plot results
    fig = go.Figure(
            go.Scatter(
                mode = 'markers',
                marker_symbol = "square", 
                marker_size = 10,
                marker_color = "#81B4E3",
                marker_line_width = 2,
                marker_line_color = "black",
                x = barchart_df,
                y = height_df,
                hovertemplate = (
                    '<br><b>Personne </b>: %{text}<br>'+
                    '<b>Distinctions </b> : %{x}  <extra></extra>'
                ),
                text = barchart_df.index,
                showlegend = False 
                ),
            go.Layout(
                title_text = "Distribution des nombres de distinctions",
                title_x = 0.5,
                height=600,
                margin=dict(l=0,r=10),
                )
            )       

    # Adjust layout
    fig.update_layout(
        xaxis_range=[min_count - 1, max_count + 1], 
        xaxis_dtick = 1, 
        xaxis_title = "Nombre de distinctions",
        yaxis_range=[-1, max_height + 1],
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Helvetica",
        font_color="#3B3838",
    )

    return fig


def create_barchart_graph(barchart_fig):
    barchart_graph = dcc.Graph(
        figure=barchart_fig, 
        id='barchart-graph',
        style={'display': 'inline-block'},
        config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
        )
    )

    return barchart_graph


def create_empty_table_fig(distinction_df):
    fig = go.Figure(
        data=[
            go.Table(
                columnwidth = [300,50],
                header_values=["<b>Distinction</b>", "<b>Année</b>"],
                header_fill_color="#81B4E3",
                header_align='center',
            ),
        ],
        layout=go.Layout(
            height=600,
            width=450,
            margin=dict(l=5,r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family="Helvetica",
            font_color="#3B3838",
        )
    )
                
    return fig


def create_link(lienWiki,distinctionLabel):
    return '<a href="'+ lienWiki +'">' + distinctionLabel.title() + '</a>'


def create_filled_table_fig(distinction_df, name):
    # Get data for the selecteur person
    one_actor = distinction_df[distinction_df['nomComplet']==name].sort_values("date", ascending=True)
    one_actor["linkToWiki"] = one_actor.apply(lambda x: create_link(x['lienWikidata'], x['distinction']), axis=1)
    
    # Create fig
    fig = go.Figure(    
        data=[
            go.Table(
                columnwidth = [300,50],
                header_values=["<b>Distinction</b>", "<b>Année</b>"],
                header_fill_color="#81B4E3",
                header_align='center',
                cells_values=[one_actor["linkToWiki"], one_actor["annee"]],
                cells_fill_color='#E5ECF6',
                cells_align=['left','center']
            )
        ],
        layout=go.Layout(
            title_text = f"Distinctions de {name}",
            title_x = 0.5,
            font_family="Helvetica",
            font_color="#3B3838",
            height=600,
            width=450,
            margin=dict(l=0,r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )
         
    return fig


def create_barchart_table_graph(barchart_table_fig):
    barchart_table_graph = dcc.Graph(
        figure=barchart_table_fig, 
        id='barchart-table-graph',
        style={'display': 'inline-block'},
        config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
        )
    )

    return barchart_table_graph
    
def create_barchart(barchart_graph, barchart_table_graph):  # barchart_title, barchart_table_title
    
    barchart = [
            html.Div(className="graph-distinction", children=[barchart_graph]),
            html.Div(className="table-distinction",children=[barchart_table_graph]),
        ]   
    
    return barchart