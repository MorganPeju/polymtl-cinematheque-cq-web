#
# This file contains the function used as callback to interact with the visualizations. 
#


# External lib
import plotly.express as px
import plotly.graph_objects as go
import dash_html_components as html

# Local lib
from treemap import create_treemap_title
from treemap import query_data_for_treemap
from treemap import get_treemap_hover_template

from bumpchart import create_bumpchart_fig

from table import create_table_title
from table import query_data_for_table
from table import create_table_fig

from barchart import create_empty_table_fig
from barchart import create_filled_table_fig

import hbarchart

def callback_treemap(treemap_df, slider_min_year, slider_max_year, ddm_genre):
    """
    Handles the callback for the treemap

    Parameters
    ----------
    treemap_df : pd.DataFrame()
        The DataFrame containing all the data relevant for the treemap

    slider_min_year : int
        The min year selected on the slider

    slider_max_year : int
        The max year selected on the slider

    ddm_genre : str()
        The genre selected on the dropdown menu

    Raises
    ------
    -

    Returns
    -------
    treemap_fig : plotly.graph_object.Figure()
        The treemap figure

    Sources
    -------
    -

    See Also
    --------
    -
    """

    # Create new title
    treemap_title = create_treemap_title(
        year_min_displayed=slider_min_year, 
        year_max_displayed=slider_max_year, 
        genre_displayed=ddm_genre
    )
    
    # Get data
    temp_df = query_data_for_treemap(
        df=treemap_df, 
        genre=ddm_genre, 
        from_year=slider_min_year, 
        to_year=slider_max_year
    )

    # Create a figure with px
    treemap_fig = px.treemap(
        temp_df, 
        path=['planete', 'continent', 'pays'], 
        values='nombreDeFilms',
        hover_name="pays",
        color_discrete_sequence=px.colors.sequential.BuPu,
    )
    
    treemap_fig.update_traces(
        hovertemplate=get_treemap_hover_template(),
        marker_line=dict(
            color='grey'
        )
    )
    treemap_fig.update_layout(
        #height=500,
        margin=dict(l=0,r=0,b=20,t=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return treemap_title, treemap_fig


def callback_bumpchart(bumpchart_df, ddm_genre):

    fig = create_bumpchart_fig(bumpchart_df=bumpchart_df)

    if ddm_genre == "All":
        return fig
    else:
        fig = fig.update_traces(
            marker_color="lightgrey",
            hoverinfo='none',
            )
        x_data = bumpchart_df["decennie"]
        y_data = bumpchart_df["rang"]
        genreCat = bumpchart_df['genre']
        
        fig.add_trace(
            go.Scatter(
                x = x_data[genreCat==str(ddm_genre)],
                y = y_data[genreCat==str(ddm_genre)],
                name=ddm_genre,
                mode='lines+markers',
                marker_symbol='square',
                marker_color='red',
                marker_size=10,
                hoverinfo='skip',
            )
        )

        return fig


def callback_table(table_df, slider_min_year, slider_max_year, ddm_genre, top_n):
    
    # Create new title
    table_title= create_table_title(
        year_min_displayed=slider_min_year, 
        year_max_displayed=slider_max_year, 
        genre_displayed=ddm_genre,
        top_n=top_n
    )
    # Get data
    top_n_df, oldest_df, latest_df = query_data_for_table(
        table_df=table_df, 
        genre=ddm_genre, 
        from_year=slider_min_year,
        to_year=slider_max_year, 
        top_n=top_n
    )

    # Create a fig
    table_top_n_fig, table_latest_fig, table_oldest_fig = create_table_fig(
        top_n_df=top_n_df,
        oldest_df=oldest_df, 
        latest_df=latest_df,
        top_n=top_n
    )

    return table_title, table_top_n_fig, table_latest_fig, table_oldest_fig


def callback_barchart(distinction_df, barchart_click):

    if barchart_click is None:
        return create_empty_table_fig(distinction_df=distinction_df)
    else:
        return create_filled_table_fig(distinction_df=distinction_df, name=barchart_click['points'][0]['text']) 

def callback_hbarchart(h_barchart_ddm, h_barchart_df, avg_df):
    fig = hbarchart.create_h_barchart_fig(h_barchart_ddm, h_barchart_df, avg_df)

    return fig