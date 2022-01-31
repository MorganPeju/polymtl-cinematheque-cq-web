#
# This file contains the functions used to preprocess data for the sunburst
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
import preprocess_vsCommon as common


def clean_duplicates_for_sunburst(df):
    # Drop duplicates due to irrelevant fields
    temp_df = df.drop_duplicates(
        subset=['titreOriginal', 'anneeSortie', 'genre', 'sousGenre0', 'sousGenre1'],
        keep='first'
    )

    return temp_df


def clean_genre_column_for_sunburst(df):
    # Capture the lenght before dropping
    initial_length = len(df)

    # Drop movies for which no genre is available
    temp_df = df.dropna(subset=['genre'])
    
    # Capture the lenght after dropping
    after_drop_length = len(temp_df)
    
    # Set missing values
    #temp_df["sousGenre0"] = temp_df["sousGenre0"].fillna("n.d.")
    #temp_df["sousGenre1"] = temp_df["sousGenre1"].fillna("n.d.")
    #temp_df["sousGenre0"].fillna("n.d.", inplace=True)
    #temp_df["sousGenre1"].fillna("n.d.", inplace=True)
    temp_df = temp_df.fillna("n.d.")

    # Compute length deltas
    count_dropped_no_genre = initial_length - after_drop_length
    
    return temp_df, count_dropped_no_genre


def clean_genre_label_column_for_sunburst(df):
    
    # Explicit copy
    temp_df = df.copy()

    # Replace strings 'VIDÉOS|VIDÉO' for 'Vidéos'
    temp_df = common.replace_str_containing_str(
        df=temp_df, 
        column_name='genreIdentifiant', 
        search_str='VIDÉOS|VIDÉO', 
        new_str='Vidéos',
        contain_word=True
    )
    
    # Replace strings 'ÉMISSIONS' for 'Émissions'
    temp_df = common.replace_str_containing_str(
        df=temp_df, 
        column_name='genreIdentifiant', 
        search_str='ÉMISSIONS', 
        new_str='Émissions',
        contain_word=True
    )
    
    # Replace strings 'TV' for 'TV'
    temp_df = common.replace_str_containing_str(
        df=temp_df, 
        column_name='genreIdentifiant', 
        search_str='TV', 
        new_str='TV',
        contain_word=True
    )
    
    # Replace strings that do not contain 'Vidéos|Émissions|TV' for 'Films'
    temp_df = common.replace_str_containing_str(
        df=temp_df, 
        column_name='genreIdentifiant', 
        search_str='Vidéos|Émissions|TV', 
        new_str='Films',
        contain_word=False
    )

    return temp_df


def clean_film_df_for_sunburst(film_df):
    
    # Explicit copy
    temp_df = film_df.copy()
    
    # Clean duplicates, year, title and genre
    temp_df = clean_duplicates_for_sunburst(df=temp_df)
    temp_df, count_dropped_no_title = common.clean_title_column(df=temp_df)
    temp_df, count_dropped_no_year, count_filtered_year_greater_now = common.clean_year_column(df=temp_df)
    temp_df, count_dropped_no_genre = clean_genre_column_for_sunburst(df=temp_df)
    
    # Capitalize genre
    temp_df = common.capitalize_all_letter_all_words(df=temp_df, col_name="genre")
    
    # Clean genre label
    temp_df = clean_genre_label_column_for_sunburst(df=temp_df)

    # Select only relevant columns
    temp_df = temp_df[['titreOriginal', 'genre', 'sousGenre0', 'sousGenre1']]

    return temp_df
