#
# This file contains the functions used to preprocess data for the bar
#


# External lib
import numpy as np
import pandas as pd


# Internal lib
import preprocess_vsCommon as common


def clean_distinction_df(raw_distinction_df):
    
    def extract_date(x):
        if x != np.nan:
            return pd.to_datetime(x.split("T")[0], format="%Y-%m-%d", errors='coerce')
        else:
            return x
        
    # Drop error on line 1176
    temp_df = raw_distinction_df.drop([1176])
    
    # Drop unnecessary columns
    temp_df = temp_df.drop(columns=['person'])
    
    # Rename columns
    temp_df = temp_df.rename(
        columns={
            'personLabel': 'nomComplet', 
            'distinctionLabel': 'distinction',
            'distinction': 'lienWikidata'
        }
    )
    
    # Drop nobody
    temp_df = temp_df.dropna(subset=['nomComplet'])

    # Extract date
    temp_df['date'] = temp_df['date'].apply(lambda x : extract_date(x))
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    
    # Extract year
    temp_df['annee'] = temp_df['date'].apply(lambda x: x.year)
    temp_df['annee'] = temp_df['annee'].astype('Int32')

    return temp_df


def clean_distinction_df_for_barchart(distinction_df):
    
    # Get number of dinstinctions / person
    temp_df = distinction_df.groupby("nomComplet")["date"].count()

    # Drop person with less than 5 distinction - they are not cool enough
    temp_df = temp_df.loc[temp_df >= 5]

    return temp_df