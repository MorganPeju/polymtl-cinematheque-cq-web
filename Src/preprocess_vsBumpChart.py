#
# This file contains the functions used to preprocess data for the bumpchart 
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
import preprocess_vsCommon as common


def clean_duplicates_for_bumpchart(df):
    # Drop duplicates due to irrelevant fields
    temp_df = df.drop_duplicates(
        subset=['titreOriginal','anneeSortie', 'genre'], 
        keep='first'
    )

    # Drop duplicates due to 'genre'
    temp_df = df.drop_duplicates(
        subset=['titreOriginal','anneeSortie'], 
        keep='first'
    )

    return temp_df


def clean_genre_column_for_bumpchart(df):
    # Capture the lenght before dropping
    initial_length = len(df)

    # Drop movies for which no genre is available
    temp_df = df.dropna(subset=['genre'])
    
    # Capture the lenght after dropping
    after_drop_length = len(temp_df)
    
    # Replace value
    #temp_df["genre"] = temp_df["genre"].replace("FICTION SPÉCULATIVE","SCIENCE FICTION")
    temp_df["genre"].replace("FICTION SPÉCULATIVE","SCIENCE FICTION", inplace=True)
    
    # Compute length deltas
    count_dropped_no_genre = initial_length - after_drop_length
    
    return temp_df, count_dropped_no_genre   


def clean_year_column_for_bumpchart(df):
    # Capture the lenght before dropping
    initial_length = len(df)
    
    # Drop movies for which no date is available
    temp_df = df.dropna(subset=['anneeSortie'])
    
    # Capture the lenght after dropping
    after_drop_year_length = len(temp_df)
    
    # Cast years to type int
    temp_df = temp_df.astype({'anneeSortie': 'int'})
    
    # Filter movies for which date is <= 1900 or > than now
    temp_df = temp_df[temp_df['anneeSortie']>1900]
    temp_df = temp_df[temp_df['anneeSortie']<=datetime.datetime.now().year]
    
    # Capture the length after filtering
    after_filter_length = len(temp_df)
    
    # Compute length deltas
    count_dropped_no_year = initial_length - after_drop_year_length
    count_filtered_year_greater_now = after_drop_year_length - after_filter_length
    
    return temp_df, count_dropped_no_year, count_filtered_year_greater_now


def clean_film_df_for_bumpchart(film_df):
    
    # Explicit copy
    temp_df = film_df.copy()
    
    # Clean duplicates, year, title and genre
    temp_df = clean_duplicates_for_bumpchart(df=temp_df)
    temp_df, count_dropped_no_title = common.clean_title_column(df=temp_df)
    temp_df, count_dropped_no_year, count_filtered_year_greater_now = clean_year_column_for_bumpchart(df=temp_df)
    temp_df, count_dropped_no_genre = clean_genre_column_for_bumpchart(df=temp_df)

    return temp_df


def add_decade_column_for_bumpchart(df):
    
    # Order film
    temp_df = df.sort_values(by="anneeSortie")

    # Create decades
    decades = np.arange(1900, 2019+(10-(2019%10)+1), 10)

    # Add a 'decade' column
    for decade in decades:
        temp_df.loc[(temp_df['anneeSortie'] > decade) & (temp_df['anneeSortie'] <= (decade+10)), 'decennie'] = decade+10

    # Set dtype for 'decennie'
    temp_df['decennie'] = temp_df['decennie'].astype(int)

    return temp_df
    

def create_genre_rank_for_bumpchart(df):
    
    # Group by decade
    temp_df = (df
        .groupby(['decennie','genre'])
        .size()
        .reset_index(name="compte")
    )

    # Sort each decade
    temp_df = (temp_df
        .groupby(['decennie'])
        .apply(lambda x: x.sort_values(["compte"], ascending=False))
        .reset_index(drop=True)
    )

    # Add a rank column
    temp_df["rang"] = (temp_df
        .groupby('decennie')["compte"]
        .rank(method="first", ascending=False)
    )
    
    # Cast rank to int
    temp_df["rang"] = temp_df["rang"].astype(int)
    #temp_df.rang = temp_df.rang.astype(int)

    return temp_df


def prepare_data_for_bumpchart(raw_bumpchart_df):

    # Add decade
    temp_df = add_decade_column_for_bumpchart(df=raw_bumpchart_df)   

    # Create rank
    temp_df = create_genre_rank_for_bumpchart(df=temp_df) 
    
    return temp_df