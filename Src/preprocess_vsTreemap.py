#
# This file contains the functions used to preprocess data for the treemap
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
import preprocess_vsCommon as common


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

    def extract_country(x):
        temp = x.split(',')
        if len(temp)==2:
            return temp[0]
        else:
            return x
    
    # Set missing values
    temp_df['pays'] = temp_df['pays'].fillna("n.d.")
    
    # Extract country 
    temp_df['pays'] = temp_df['pays'].apply(lambda x: extract_country(x))

    # Set missing continents
    temp_df = temp_df.drop(temp_df[temp_df['continent']==""].index)
    
    return temp_df


def create_treemap_df(raw_bumpchart_df):
    # Extract relevant columns
    temp_df = raw_bumpchart_df[['titreOriginal', 'anneeSortie', 'planete', 'continent', 'pays', 'genre']]

    # Drop duplicates 
    temp_df = temp_df.drop_duplicates()

    # Clean country column
    temp_df = clean_country_column_for_treemap(df=temp_df)
    
    return temp_df