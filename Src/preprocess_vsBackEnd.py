#
# This file contains the functions to process the data from the Cinematheque db
#


# External lib
import numpy as np
import pandas as pd
import datetime


# Internal lib
import preprocess_vsCommon


# Global variable
relative_path = "./Src/assets/data/"

def backend_load_film():
    # Set file path and name
    file_name = "film.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
    )
    
    return temp_df


def backend_load_genre():
    # Set file path and name
    file_name = "film_genre.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_film_language():
    # Set file path and name
    file_name = "film_langue.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_language():
    # Set file path and name
    file_name = "langue.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_film_country():
    # Set file path and name
    file_name = "film_pays.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_country():
    # Set file path and name
    file_name = "pays.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_continent():
    # Set file path and name
    file_name = "continent.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_director():
    # Set file path and name
    file_name = "film_directeur.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_name():
    # Set file path and name
    file_name = "nom.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_realisator():
    # Set file path and name
    relative_path = "./Assets/Data/Jc/"
    file_name = "film_realisateur.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_function():
    # Set file path and name
    file_name = "fonction.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_generic():
    # Set file path and name
    file_name = "film_generique.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_film_genre_category():
    # Set file path and name
    file_name = "film_genreCategorie.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_genre_category_wiki():
    # Set file path and name
    file_name = "genreCategorie_wikidata.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def backend_load_film_genre():
    # Set file path and name
    file_name = "film_genre.csv"
    full_path = relative_path + file_name
    
    # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )
    
    return temp_df


def load_genre_hierarchy(): 
    # Set file path and name
    file_name = "genre_hierarchie.csv"
    full_path = relative_path + file_name
    
     # Read csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=r'[";]',
        engine='python',
        header=0,
    )
    
    hierarchy_df = temp_df.drop(temp_df.columns[[0, -1]], axis=1)
    hierarchy_df = hierarchy_df.fillna(value="")

    return hierarchy_df


def backend_load_distinction():
    # Set file path and name
    file_name = "distinction.csv"
    full_path = relative_path + file_name

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        parse_dates=True,
    )

    return temp_df


def merge_film_and_generic(film_df, generic_df):
    temp_df = pd.merge(
        left=film_df,
        right=generic_df,
        how="left",
        left_on="FilmoId",
        right_on="filmoId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_function(film_df, function_df):
    temp_df = pd.merge(
        left=film_df,
        right=function_df,
        how="left",
        left_on="fonctionId",
        right_on="FonctionId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_name(film_df, name_df):
    temp_df = pd.merge(
        left=film_df,
        right=name_df,
        how="left",
        left_on="nomId",
        right_on="NomId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_film_language(film_df, film_language_df):
    temp_df = pd.merge(
        left=film_df,
        right=film_language_df,
        how="left",
        left_on="FilmoId",
        right_on="filmoId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_language(film_df, language_df):
    temp_df = pd.merge(
        left=film_df,
        right=language_df,
        how="left",
        left_on="langueId",
        right_on="LangueId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_film_country(film_df, film_country_df):
    temp_df = pd.merge(
        left=film_df,
        right=film_country_df,
        how="left",
        left_on="FilmoId",
        right_on="filmoId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_country(film_df, country_df):
    temp_df = pd.merge(
        left=film_df,
        right=country_df,
        how="left",
        left_on="paysId",
        right_on="PaysId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_continent(film_df, continent_df):
    temp_df = pd.merge(
        left=film_df,
        right=continent_df,
        how="left",
        left_on="pays",
        right_on="pays",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_film_genre_category(film_df, film_genre_category_df):
    temp_df = pd.merge(
        left=film_df,
        right=film_genre_category_df,
        how="left",
        left_on="FilmoId",
        right_on="filmoId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_genre_category_wiki(film_df, genre_category_wiki_df):
    temp_df = pd.merge(
        left=film_df,
        right=genre_category_wiki_df,
        how="left",
        left_on="sujetId",
        right_on="sujetId",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_film_genre(film_df, film_genre_df):
    temp_df = pd.merge(
        left=film_df,
        right=film_genre_df,
        how="left",
        left_on="lienWikidata",
        right_on="genre",
        suffixes=("", "")
    )
    
    return temp_df


def merge_film_and_genre_hierarchy(film_df, genre_hierearchy_df):
    temp_df = pd.merge(
        left=film_df,
        right=genre_hierearchy_df,
        how="left",
        left_on="genreLabel",
        right_on="data",
        suffixes=("", "")
    )
    
    return temp_df


def clean_film_df_after_load(df):
    # Drop all columns but id, title, year
    temp_df = df[['FilmoId','titreOriginal','anneeSortie']]
    
    return temp_df


def clean_film_df_after_merge_generic(df):
    # Drop 'organismeId' and 'filmoId'
    temp_df = df.drop(columns=['organismeId', 'filmoId'])
    
    return temp_df


def clean_film_df_after_merge_function(df):
    # Drop 'fonctionId' and 'FonctionId'
    temp_df = df.drop(columns=['fonctionId', 'FonctionId'])
    
    # Rename 'terme' to 'fonction'
    temp_df = temp_df.rename(columns={"terme": "fonction"})
    
    return temp_df


def clean_film_df_after_merge_name(df):
    # Drop 'nomId' and 'NomId'
    temp_df = df.drop(columns=['nomId', 'NomId'])
    
    # Add a combined first name and last name column
    temp_df['nomComplet'] = temp_df['prenom'] + " " + temp_df['nom']
    
    return temp_df


def clean_film_df_after_merge_film_language(df):
    # Drop 'filmoId' 
    temp_df = df.drop(columns=['filmoId'])
    
    return temp_df


def clean_film_df_after_merge_language(df):
    # Drop 'langueId' and 'LangueId' 
    temp_df = df.drop(columns=['langueId', 'LangueId'])
    
    # Rename 'terme' to 'langue'
    temp_df = temp_df.rename(columns={"terme": "langue"})
    
    return temp_df


def clean_film_df_after_merge_film_country(df):
    # Drop 'filmoId' 
    temp_df = df.drop(columns=['filmoId'])
    
    return temp_df


def clean_film_df_after_merge_country(df):
    # Drop 'paysId' and 'PaysId' 
    temp_df = df.drop(columns=['paysId', 'PaysId'])
    
    # Rename 'terme' to 'pays'
    temp_df = temp_df.rename(columns={"terme": "pays"})
    
    return temp_df


def clean_film_df_after_merge_continent(df):
    # Drop none
    temp_df = df
    
    return temp_df


def clean_film_df_after_merge_film_genre_category(df):
    # Drop 'filmoId', 'FilmoGenresCategoriesID'
    temp_df = df.drop(columns=['filmoId', 'FilmoGenresCategoriesID'])
    
    return temp_df


def clean_film_df_after_merge_genre_category_wiki(df):
    # Drop 'sujetId' and 
    temp_df = df.drop(columns=['sujetId'])
    
    return temp_df


def clean_film_df_after_merge_film_genre(df):
    # Drop 'lienWikidata', 'genre'
    temp_df = df.drop(columns=['lienWikidata', 'genre'])
      
    return temp_df


def clean_film_df_after_merge_genre_hierarchy(df):
    # Drop 'data'
    temp_df = df.drop(columns=['data'])
    
    # Rename 'genreLabel', 'subgenre_0, subgenre_1'
    temp_df = temp_df.rename(columns={
        "genreLabel": "genreIdentifiant",
        "subgenre_0": "sousGenre0",
        "subgenre_1": "sousGenre1"
    })
    
    return temp_df


def add_constant_column(df, col_name, const_name):
    # Create a copy of the given df
    temp_df = df.copy()
    
    # Add the constant col with the given name
    temp_df[col_name] = const_name
    
    return temp_df


def preprocess_film_genre(df):
    temp_df=df[['genre', 'genreLabel']]
    temp_df=temp_df.drop_duplicates()
    
    return temp_df


def create_master_film_df():
    # Load film_df
    film_df = backend_load_film()
    # Clean film_df
    film_df = clean_film_df_after_load(df=film_df)

    # Load generic_df
    generic_df = backend_load_generic()
    # Merge film_df and generic_df
    film_df = merge_film_and_generic(film_df=film_df, generic_df=generic_df)
    # Clean film_df after merge with generic_df
    film_df = clean_film_df_after_merge_generic(df=film_df)
    # Clear memory space
    del generic_df

    # Load function_df
    function_df = backend_load_function()
    # Merge film_df and function_df
    film_df = merge_film_and_function(film_df=film_df, function_df=function_df)
    # Clean film_df after merge with function_df
    film_df = clean_film_df_after_merge_function(df=film_df)
    # Clear memory space
    del function_df

    # Load name_df
    name_df = backend_load_name()
    # Merge film_df and name_df
    film_df = merge_film_and_name(film_df=film_df, name_df=name_df)
    # Clean film_df after merge with name_df
    film_df = clean_film_df_after_merge_name(df=film_df)
    # Clear memory space
    del name_df

    # Load film_language_df
    film_language_df = backend_load_film_language()
    # Merge film_df and film_langue_df
    film_df = merge_film_and_film_language(film_df=film_df, film_language_df=film_language_df)
    # Clean film_df after merge with film_langue_df
    film_df = clean_film_df_after_merge_film_language(df=film_df)
    # Clear memory space
    del film_language_df

    # Load language_df
    language_df = backend_load_language()
    # Merge film_df and language_df
    film_df = merge_film_and_language(film_df=film_df, language_df=language_df)
    # Clean film_df after merge with language_df
    film_df = clean_film_df_after_merge_language(df=film_df)
    # Clear memory space
    del language_df

    # Load film_country_df
    film_country_df = backend_load_film_country()
    # Merge film_df and film_pays_df
    film_df = merge_film_and_film_country(film_df=film_df, film_country_df=film_country_df)
    # Clean film_df after merge with film_country_df
    film_df = clean_film_df_after_merge_film_country(df=film_df)
    # Clear memory space
    del film_country_df

    # Load country_df
    country_df = backend_load_country()
    # Merge film_df and film_pays_df
    film_df = merge_film_and_country(film_df=film_df, country_df=country_df)
    # Clean film_df after merge with country_df
    film_df = clean_film_df_after_merge_country(df=film_df)
    # Clear memory space
    del country_df

    # Load continent_df
    continent_df = backend_load_continent()
    # Merge film_df and film_pays_df
    film_df = merge_film_and_continent(film_df=film_df, continent_df=continent_df)
    # Clean film_df after merge with continent_df
    film_df = clean_film_df_after_merge_continent(df=film_df)
    # Clear memory space
    del continent_df

    # Add planete column
    film_df = add_constant_column(df=film_df, col_name='planete', const_name='Terre')

    # Load film_genre_category_df
    film_genre_category_df = backend_load_film_genre_category()
    # Merge film_df and film_genre_category_df
    film_df = merge_film_and_film_genre_category(film_df=film_df, film_genre_category_df=film_genre_category_df)
    # Clean film_df after merge with film_genre_category_df
    film_df = clean_film_df_after_merge_film_genre_category(df=film_df)
    # Clear memory space
    del film_genre_category_df

    # Load genre_category_wiki_df
    genre_category_wiki_df = backend_load_genre_category_wiki()
    # Merge film_df and genre_category_wiki_df
    film_df = merge_film_and_genre_category_wiki(film_df=film_df, genre_category_wiki_df=genre_category_wiki_df)
    # Clean film_df after merge with genre_category_wiki_df
    film_df = clean_film_df_after_merge_genre_category_wiki(df=film_df)
    # Clear memory space
    del genre_category_wiki_df

    # Load film_genre_df
    film_genre_df = backend_load_film_genre()
    # Preprocess film_genre_df
    film_genre_df = preprocess_film_genre(df=film_genre_df)
    # Merge film_df and film_genre_df
    film_df = merge_film_and_film_genre(film_df=film_df, film_genre_df=film_genre_df)
    # Clean film_df after merge with film_genre_df
    film_df = clean_film_df_after_merge_film_genre(df=film_df)
    # Clear memory space
    del film_genre_df

    # Load genre_hierearchy_df
    genre_hierearchy_df = load_genre_hierarchy()
    # Merge film_df and genre_hierearchy_df
    film_df = merge_film_and_genre_hierarchy(film_df=film_df, genre_hierearchy_df=genre_hierearchy_df)
    # Clean film_df after merge with genre_hierearchy_df
    film_df = clean_film_df_after_merge_genre_hierarchy(df=film_df)
    # Clear memory space
    del genre_hierearchy_df
    
    return film_df


def clean_film_df_columns(raw_film_df):

    # Explicit copy 
    temp_df = raw_film_df.copy()

    # clean str columns
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='titreOriginal')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='fonction')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='nom')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='prenom')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='nomComplet')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='langue')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='pays')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='continent')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='capitale')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='planete')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='genreIdentifiant')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='genre')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='sousGenre0')
    temp_df = preprocess_vsCommon.clean_str_column(df=temp_df, col_name='sousGenre1')
    
    # capitalize 
    temp_df = preprocess_vsCommon.capitalize_first_letter_all_words(df=temp_df, col_name='titreOriginal')
    temp_df = preprocess_vsCommon.capitalize_first_letter_all_words(df=temp_df, col_name='sousGenre0')
    temp_df = preprocess_vsCommon.capitalize_first_letter_all_words(df=temp_df, col_name='sousGenre1')
    
    return temp_df


def create_file_from_df(df, file_name):
    # Set file path and name
    full_path = relative_path + file_name
    
    # Write csv
    df.to_csv(
        path_or_buf=full_path,
        sep=',',
        index=False
    )
    
    return


def load_preprocessed_file(file_name):
    # Set file path and name
    file_name = file_name
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0
    )

    return temp_df


def load_master_film_file():

    # Set file path and name
    file_name = "film_vsMaitre.csv"
    full_path = relative_path + file_name

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        low_memory=False,
        dtype={
            'FilmoId': int,
            'titreOriginal': str,
            'anneeSortie': int,
            'GeneriqueId': float,
            'fonction': str,
            'nom': str,
            'prenom': str,
            'nomComplet': str,
            'langue': str,
            'pays': str,
            'continent': str,
            'capitale': str,
            'planete': str,
            'genreIdentifiant': str,
            'genre': str,
            'sousGenre0': str,
            'sousGenre1': str
        }
    )

    # Make sure missing value are None
    temp_df = temp_df.replace(r'^\s*$', None, regex=True)
    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df


def load_preprocessed_avg_file():
    # Set file path and name
    file_name = "p_avg.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'genre': str,
            'moyenne': float,
        }
    )

    # Set type
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df


def load_preprocessed_distinction_file():
    # Set file path and name
    file_name = "p_distinction.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        parse_dates=['date'],
        dtype={
            'nomComplet': str,
            'distinction': str,
            'date': str,
            'annee': 'Int64'
        }
    )

    return temp_df


def load_preprocessed_bumpchart_file():
    # Set file path and name
    file_name = "p_bumpchart.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'decennie': 'Int64',
            'genre': str,
            'compte': 'Int64',
            'rang': 'Int64',
        }
    )

    # Set type
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df


def load_preprocessed_h_barchart_file():
    # Set file path and name
    file_name = "p_h_barchart.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'nomComplet': str,
            'genre': str,
            'nombreDeFilms': 'Int64',
        }
    )

    # Set type
    temp_df['nomComplet'] = temp_df['nomComplet'].fillna("n.d.")
    temp_df['nomComplet'] = temp_df['nomComplet'].str.title()
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")
    return temp_df


def load_preprocessed_sunburst_file():
    # Set file path and name
    file_name = "p_sunburst.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'titreOriginal': str,
            'genre': str,
            'sousGenre0': str,
            'sousGenre1': str,
        }
    )

    # Set type
    temp_df['titreOriginal'] = temp_df['titreOriginal'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")
    temp_df['sousGenre0'] = temp_df['sousGenre0'].fillna("n.d.")
    temp_df['sousGenre1'] = temp_df['sousGenre1'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df


def load_preprocessed_table_file():
    # Set file path and name
    file_name = "p_table.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'titreOriginal': str,
            'anneeSortie': 'Int64',
            'langue': str,
            'genre': str,
        }
    )

    # Set type
    temp_df['titreOriginal'] = temp_df['titreOriginal'].fillna("n.d.")
    temp_df['langue'] = temp_df['langue'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")

    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df


def load_preprocessed_treemap_file():
    # Set file path and name
    file_name = "p_treemap.csv"
    full_path = relative_path + file_name 

    # Read .csv
    temp_df = pd.read_csv(
        filepath_or_buffer=full_path,
        sep=',',
        header=0,
        dtype={
            'titreOriginal': str,
            'anneeSortie': 'Int64',
            'planete': str,
            'continent': str,
            'pays':str,
            'genre':str,
        }
    )

    # Set type
    temp_df['titreOriginal'] = temp_df['titreOriginal'].fillna("n.d.")
    temp_df['planete'] = temp_df['planete'].fillna("n.d.")
    temp_df['continent'] = temp_df['continent'].fillna("n.d.")
    temp_df['pays'] = temp_df['pays'].fillna("n.d.")
    temp_df['genre'] = temp_df['genre'].fillna("n.d.")

    temp_df['genre'] = temp_df['genre'].replace(['Sf'],'SF')
    return temp_df