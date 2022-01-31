#
# This file contains the functions used to preprocess data for the bar
#


# External lib
import numpy as np
import pandas as pd


# Internal lib
import preprocess_vsCommon as common



def clean_duplicates_for_h_barchart(df):

    # Drop duplicates due to irrelevant fields
    temp_df = df.drop_duplicates(
        subset=['titreOriginal','anneeSortie', 'genre', 'fonction', 'nomComplet'], 
        keep='first'
    )

    return temp_df


def clean_film_df_for_h_barchart(film_df):
    # Explicit copy
    temp_df = film_df.copy()
    
    # Get producers
    temp_df = temp_df[temp_df["fonction"] == "Producteur"]
    
    # Clean duplicates, year, title and genre
    temp_df = clean_duplicates_for_h_barchart(df=temp_df)
    #temp_df, count_dropped_no_title = common.clean_title_column(df=temp_df)
    #temp_df, count_dropped_no_year, count_filtered_year_greater_now = clean_year_column_for_bumpchart(df=temp_df)
    #temp_df, count_dropped_no_genre = clean_genre_column_for_bumpchart(df=temp_df)

    return temp_df


def create_h_barchart_df(raw_h_barchart_df):
    
    temp_df = raw_h_barchart_df.copy()
    
    temp_df["value"] = 1
    
    temp_df = (
        pd.pivot_table(
            temp_df, 
            values="value", 
            index=["nomComplet", "titreOriginal"], 
            columns="genre"
        )
        .fillna(0)
        .groupby("nomComplet")
        .agg(sum)
        .reset_index()
        .melt(
            id_vars=['nomComplet'], 
            var_name=None, 
            value_name='nombreDeFilms'
        )
    )
    
    return temp_df  


def create_average_df_for_h_barchart(h_barchart_df):
    # Compute average
    temp_df = (h_barchart_df
        .groupby('genre')
        .agg(moyenne=pd.NamedAgg(column='nombreDeFilms', aggfunc='sum')) 
        / len(h_barchart_df['nomComplet'].unique())
    )
    
    temp_df = temp_df.reset_index()

    return temp_df 
