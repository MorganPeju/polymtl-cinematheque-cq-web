#
# This file contains the functions used for preprocess
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
# none


def set_dtype_to_int(x):
    if x != np.nan:
        return int(x)
    else:
         return x


def set_dtype_to_str(x):
    if x != np.nan:
        return str(x)
    else:
         return x


def strip_decimals_and_set_dtype_to_int(x):
    if x != np.nan:
        return str(x)
    else:
         return x


def capitalize_first_letter_first_word(df, col_name):
    temp_df = df.copy()
    temp_df[col_name] = temp_df[col_name].apply(str.capitalize)

    return temp_df


def capitalize_first_letter_all_words(df, col_name):
    temp_df = df.copy()
    temp_df[col_name] = temp_df[col_name].apply(str.title)
    
    return temp_df


def capitalize_all_letter_all_words(df, col_name):
    temp_df = df.copy()
    temp_df[col_name] = temp_df[col_name].apply(str.upper)
    
    return temp_df


def clean_str_column(df, col_name):
    
    # Make a local copy
    temp_df = df.copy()

    temp_df[col_name] = (temp_df[col_name]
        .apply(lambda x: str.capitalize(x) if isinstance(x, str) else str(""))
    )
    
    return temp_df


def replace_str_containing_str(df, column_name, search_str, new_str, contain_word):
    '''
    Si contain_word = True: 
        Cette fonction permet de remplacer les cellules d'un 
        dataframe contenant certains mots par un autre.
        
    Si contain_word = False: 
        Cette fonction permet de remplacer les cellules d'un 
        dataframe NE contenant PAS certains mots par un autre.
    
    Retourne : 
    Le Dataframe modifié
    '''
    
    # Make a local copy 
    temp_df = df.copy()
    
    # Replace string
    if  contain_word == True:
        temp_df.loc[temp_df[column_name].str.contains(search_str, case=False), column_name] = new_str
        
    elif contain_word == False:
        temp_df.loc[~temp_df[column_name].str.contains(search_str, case=False), column_name] = new_str
    
    return temp_df


def round_col_decimals(df, col_name, n_decimals):
    # Round the col_name of the dataframe
    temp_df = df[col_name].round(decimals=n_decimals)
    
    return temp_df


def round_decimals(df, n_decimals):
    # Round the dataframe
    temp_df = df.round(decimals=n_decimals)
    
    return temp_df


def get_min_and_max_year(df):
    """
    Gets the minimum and the maximum year of the column year, i.e. annee, of a given df

    Parameters
    ----------
    -

    Raises
    ------
    -

    Returns
    -------
    year_min : int
        The minimum year

    year_max : int
        The maximum year    

    Sources
    -------
    -

    See Also
    --------
    -
    """

    year_max = df['anneeSortie'].max()
    year_min = df['anneeSortie'].min()
    
    return year_min, year_max


def get_list_of_genres(df):
    """
    Extract a list of genres from the "genre" column of a given df

    Parameters
    ----------
    -

    Raises
    ------
    -

    Returns
    -------
    genres : list()
        The list of genres   

    Sources
    -------
    -

    See Also
    --------
    -
    """
    
    genres = list(set(df['genre'].values))
    
    return genres


def clean_year_column(df):
    # Capture the lenght before dropping
    initial_length = len(df)
    
    # Drop movies for which no date is available
    temp_df = df.dropna(subset=['anneeSortie'])
    
    # Capture the lenght after dropping
    after_drop_length = len(temp_df)
    
    # Cast years to type int
    temp_df = temp_df.astype({'anneeSortie': 'int'})
    
    # Filter movies for which date is greater than now
    temp_df = temp_df[temp_df['anneeSortie']<=datetime.datetime.now().year]
    
    # Capture the length after filtering
    after_filter_length = len(temp_df)
    
    # Compute length deltas
    count_dropped_no_year = initial_length - after_drop_length
    count_filtered_year_greater_now = after_drop_length - after_filter_length
    
    return temp_df, count_dropped_no_year, count_filtered_year_greater_now


def clean_title_column(df):
    # Capture the lenght before dropping missing titles
    initial_length = len(df)

    # Drop movies for which no title is available
    temp_df = df.dropna(subset=['titreOriginal'])
    
    # Capture the lenght after dropping
    after_drop_length = len(temp_df)
    
    # Cast titles to type str
    #temp_df = temp_df.astype({'titreOriginal': 'str'})
    
    # Compute length deltas
    count_dropped_no_title = initial_length - after_drop_length
    
    return temp_df, count_dropped_no_title

