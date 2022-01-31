import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc


import plotly.io as pio


def remove_empty_duplicates(df):
    '''
    Cette fonction permet de retirer les doublons pour les films qui 
    apparaissent à la fois en 'catégorisé' et 'non catégorisé'.
    Exemple: 
    (1) titre_film_1/genre_DOCUMENTAIRE/sousGenre0_Nature/sousGenre1_None
    (2) titre_film_1/genre_AUTRES/sousGenre0_Institutionnel/sousGenre1_éducatif
    (3) titre_film_1/genre_None/sousGenre0_None/sousGenre1_None
    --> La fonction retire la ligne (3)
    Retourne:
    Dataframe nettoyé
    '''

    df = df.replace(np.nan, '.', regex=True)
    df = df.sort_values(by=['titreOriginal', 'genre'], ascending=True)
    df_duplicate_temp = df[df.duplicated(subset=['titreOriginal'], keep='last')]
    index_empty_duplicates = df_duplicate_temp[df_duplicate_temp['genre']=='.'].index
    df = df.drop(index_empty_duplicates)
    
    return df

def load_movie_data():
    '''
    Cette fonction permet le chargement du fichier de données
    "films" dont nous disposons.
    
    Retourne : 
    Dataframe avec la liste des films
    '''
    # Chargement d u de films
    df = pd.read_csv('./Src/assets/data/p_sunburst.csv')
    # On met le niveau 2 en minuscule pour éviter les conflits avec le niveau 1
    df['sousGenre1'] = df['sousGenre1'].str.lower()
    df = remove_empty_duplicates(df)
    return df

def sunburst_preprocess(df_movies):
    '''
    Cette fonction permet le pretraitement des données pour
    correspondre la structure du Sunburst de Plotly.
    Autrement dit, il faut construire: 
        - Une liste des labels de TOUS les niveaux de genre
        - Une liste avec le 'parent' de chacun des labels
        - Une liste avec les valeurs de chacun des labels
    
    Retourne:
        - Un dataframe avec l'ensemble des films avec les différents
        'niveaux de genres' auxquels ils appartiennent.
        - Un dataframe avec les données pour le sunburst.
    '''
    
    # On replace les valeurs vides par "." faciliter le traitement qui suit
    df_movies_genres = df_movies.replace(np.nan, '.', regex=True)
    
    # Pour chaque niveau, on groupe les élements
    list_genre = df_movies_genres.groupby(['genre']).size()
    list_subgenre0 = df_movies_genres.groupby(['sousGenre0']).size().drop('.')
    list_subgenre1 = df_movies_genres.groupby(['sousGenre1']).size().drop('.')
    
    # On récupère une liste de valeurs pour chaque niveau 
    list_genre_values = list_genre.to_list()
    list_subgenre0_values = list_subgenre0.to_list()
    list_subgenre1_values = list_subgenre1.to_list()
    # On concatène les listes valeurs
    list_values = [*list_genre_values, *list_subgenre0_values, *list_subgenre1_values] 
    
    # On récupère une liste des labels des éléments pour chaque niveau
    # En prenant les index du dataframe on s'assure de conserver l'ordre
    list_genre_labels = list_genre.index.values.tolist()
    list_subgenre0_labels = list_subgenre0.index.values.tolist()
    list_subgenre1_labels = list_subgenre1.index.values.tolist()
    # On concatène les listes de labels
    list_labels = [*list_genre_labels, *list_subgenre0_labels, *list_subgenre1_labels] 
    
    # On récupère une liste des parents des éléments pour chaque niveau
    # En prenant les index du dataframe on s'assure de conserver l'ordre
    list_genre_parents = [''] * len(list_genre_values) # Le niveau 1 n'a pas de parents
    list_subgenre0_tuples = df_movies_genres.groupby(['sousGenre0', 'genre']).size().drop('.').index.values
    list_subgenre0_parents = [i[1] for i in list_subgenre0_tuples]
    list_subgenre1_tuples = df_movies_genres.groupby(['sousGenre1', 'sousGenre0']).size().drop('.').index.values
    list_subgenre1_parents = [i[1] for i in list_subgenre1_tuples]
    # On concatène les listes de parents
    list_parents = [*list_genre_parents, *list_subgenre0_parents, *list_subgenre1_parents] 
    
    # Code qui permet de s'assurer qu'on a bien le même nombre de valeurs pour tous les éléments
    #print('genre: values {0}, parents {1}, labels {2}'.format(len(list_genre_values), len(list_genre_parents),len(list_genre_labels)))
    #print('subgenre_0: values {0}, parents {1}, labels {2}'.format(len(list_subgenre0_values), len(list_subgenre0_parents),len(list_subgenre0_labels)))
    #print('subgenre_1: values {0}, parents {1}, labels {2}'.format(len(list_subgenre1_values), len(list_subgenre1_parents),len(list_subgenre1_labels)))
    #print(len(list_values), len(list_labels), len(list_parents))
    
    # On construit un dataframe qui permet pour visualiser la hierarchie
    dict = {'labels': list_labels, 'parents': list_parents, 'values': list_values} 
    df_sunburst = pd.DataFrame(dict)
    
    n_uncategorized_films = df_sunburst[df_sunburst['labels'] == '.']['values'].values[0]
    
    df_sunburst = df_sunburst[df_sunburst['labels'] != '.']
    
    return df_movies_genres, df_sunburst, n_uncategorized_films

def get_genre_percent(df_movies_genres, genre_level):
    '''
    Cette fonction permet de calculer, pour les labels d'un
    niveau de la hierarchie choisi, le pourcentage des différents
    types de production (Vidéos, Emissions, TV, Films).
    
    Note:
    Etant donné la grande diversité des types de productions 
    dans les données brutes, lorsque nous n'avons pas l'information
    nous avons considéré la production comme un 'Films'. 
    
    Retourne:
    Un dataframe avec les pourcentages des différents types de production
    '''

    # On compte le nombre pour chaque type de productions selon le genre
    df_temp1 = df_movies_genres.groupby([genre_level,'genreIdentifiant']).size().reset_index(name='count')
    # On compte le nombre de production total selon le genre
    df_temp2 = df_movies_genres.groupby([genre_level]).size().reset_index(name='total')
    # On concatène dans un même dataframe et on calcule le pourcentage
    df_temp = pd.merge(df_temp1, df_temp2,on =genre_level, how ='inner')
    df_temp['percent'] = df_temp['count'].div(df_temp['total'], axis=0)
    
    # On construit un dictionnaire de la forme {'type_de_prod_1' : pourcentage, 'type_de_prod_2': pourcentage}
    # Cela nous servira afficher ces données dans le hover. 
    df_temp = df_temp.groupby(genre_level).agg({'genreIdentifiant':lambda x: list(x),'percent':lambda x: list(x)}).reset_index()
    df_temp['dict_percent'] = list(zip(df_temp['genreIdentifiant'], df_temp['percent']))
    df_temp['dict_percent'] = df_temp['dict_percent'].apply(lambda x: dict(zip(x[0],x[1])))
    df_temp = df_temp[[genre_level,'dict_percent']]
    
    df_temp = df_temp[df_temp[genre_level] != '.']
    
    return df_temp

def get_hovertemplate_percent_list(df_movies_genres, genre_level_1, genre_level_2, genre_level_3):
    '''
    Cette fonction permet de créer la liste des données
    des différents types de production qui est à afficher
    dans le hover du sunburst.
    
    Retourne:
    Une liste du texte des hover de chacun des labels du 
    Sunburst.
    '''
    # Pour chacun des niveaux hierarchiques, on récupère les pourcentages
    list_genre1 = get_genre_percent(df_movies_genres,genre_level_1)['dict_percent'].to_list()
    list_genre2 = get_genre_percent(df_movies_genres,genre_level_2)['dict_percent'].to_list()
    list_genre3 = get_genre_percent(df_movies_genres,genre_level_3)['dict_percent'].to_list()
    # On concatène les listes pour conserver la logique de structure des  
    # données pour le SunBurst Plotly
    list_percent = [*list_genre1, *list_genre2, *list_genre3] 
    
    # On construit la liste des textes à afficher dans le hover
    # à partir de la liste 'list_percent'
    list_hovertemplate = []
    for i in range(0, len(list_percent)):
        keys = list(list_percent[i].keys())
        values = list(list_percent[i].values())
        hover_genre_str = ''
        for j in range(0, len(keys)):
            percent = round(values[j]*100,2)
            hover_genre_str += ' - ' + keys[j] + ' : ' + str(percent)+ '%<br>'
        list_hovertemplate.append(hover_genre_str)

    return list_hovertemplate

def get_sunburst_hover_template():
    '''
    Cette fonction permet de retourner la structure
    du hover pour le sunburst.
    
    Retourne:
    Structure du hovertemplate.
    '''
    hover = '<b>%{label}</b>  <br><br>' + \
            '<b>%{value}</b> productions :<br>'+ \
            '%{customdata}'+ \
            '<extra></extra>'
    return hover


def sunburst(df, list_hovertemplate):
    '''
    Cette fonction sert à configurer le sunburst avec Plotly.
    
    Retourne:
    La figure Sunburst à afficher
    '''
    # Initialisation
    fig = go.Figure()
    theme_color = px.colors.sequential.dense
    
    # On trace le sunburst souhaité
    fig.add_trace(go.Sunburst(
        labels=df['labels'],
        parents=df['parents'],
        values=df['values'],
        branchvalues='total',
        insidetextorientation='radial',
        maxdepth=3,
        rotation=90,
        sort=True,
        customdata=list_hovertemplate,
        hovertemplate=get_sunburst_hover_template(),
        marker_colors=theme_color,
        ))

    # On met à jour les paramètres de présenation de la figure
    fig.update_layout(
        width=700,
        height=700,
        margin=dict(l=100,r=0,b=10,t=0),
        uniformtext= dict(minsize=10,mode='hide'), # FIXME PLOTLY : L'uniformisation du texte retire l'animation
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )

    return fig

def create_sunburst():
    # Chargement des données
    df_movies = load_movie_data()
    
    # Traitement des données
    df_movies_genres, df_sunburst, n_uncategorized_films = sunburst_preprocess(df_movies)
    list_hovertemplate = get_hovertemplate_percent_list(df_movies_genres, 'genre', 'sousGenre0', 'sousGenre1')
    
    # Affichage du sunburst
    sunburst_fig = sunburst(df_sunburst, list_hovertemplate)
    
    
    sunburst_graph = dcc.Graph(
        figure=sunburst_fig, 
        id='sunburst-graph',
        config=dict(
            showTips=False,
            showAxisDragHandles=False,
            displayModeBar=False
        )
    )
    return sunburst_graph