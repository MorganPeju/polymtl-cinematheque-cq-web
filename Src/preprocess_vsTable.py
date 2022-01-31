#
# This file contains the functions used to preprocess data for the table
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
import preprocess_vsCommon as common


def create_table_df(raw_bumpchart_df):
    # Extract relevant columns
    temp_df = raw_bumpchart_df[['titreOriginal', 'anneeSortie', 'langue', 'genre']]

    # Drop duplicates 
    temp_df = temp_df.drop_duplicates()
    
    return temp_df