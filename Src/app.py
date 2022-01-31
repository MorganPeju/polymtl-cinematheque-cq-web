#
# This file contains the functions to create the dashboard comtaining the different visualizations.
#


# External lib
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Local lib
import preprocess_vsHeroku
import preprocess_vsBackEnd
import preprocess_vsCommon
import preprocess_vsSunburst
import preprocess_vsBumpChart
import preprocess_vsBarChart 
import preprocess_vsHBarChart

import sunburst
import treemap
import bumpchart
import table
import barchart
import hbarchart

import callback


# Create app
app = dash.Dash(__name__)
app.title = 'INF8808 - Projet Cinematheque'

# Preprocess
preprocess_vsHeroku.create_data_files()

# load data
sunburst_df = preprocess_vsBackEnd.load_preprocessed_sunburst_file()
treemap_df = preprocess_vsBackEnd.load_preprocessed_treemap_file()
bumpchart_df = preprocess_vsBackEnd.load_preprocessed_bumpchart_file()
table_df = preprocess_vsBackEnd.load_preprocessed_table_file()
distinction_df = preprocess_vsBackEnd.load_preprocessed_distinction_file()
barchart_df = preprocess_vsBarChart.clean_distinction_df_for_barchart(distinction_df=distinction_df)
h_barchart_df = preprocess_vsBackEnd.load_preprocessed_h_barchart_file()
avg_df = preprocess_vsBackEnd.load_preprocessed_avg_file()

# Sunburst
sunburst = sunburst.create_sunburst()

# Treemap
year_min, year_max = preprocess_vsCommon.get_min_and_max_year(df=treemap_df)
genres = preprocess_vsCommon.get_list_of_genres(df=treemap_df)
treemap_fig = treemap.create_treemap_fig(df=treemap_df, year_min=year_min, year_max=year_max)
treemap_title = treemap.create_treemap_title(year_min_displayed=year_min, year_max_displayed=year_max, genre_displayed="All")
treemap_graph = treemap.create_treemap_graph(treemap_fig=treemap_fig)
treemap_ddm = treemap.create_treemap_dropdown_menu(genres=genres)
treemap_rs = treemap.create_treemap_range_slider(year_min=year_min, year_max=year_max)
treemap = treemap.create_treemap(treemap_title=treemap_title, treemap_rs=treemap_rs, treemap_ddm=treemap_ddm, treemap_graph=treemap_graph)

# Bump Chart
genres = preprocess_vsCommon.get_list_of_genres(df=bumpchart_df)
bumpchart_ddm = bumpchart.create_bumpchart_dropdown_menu(genres=genres)
bumpchart_fig = bumpchart.create_bumpchart_fig(bumpchart_df=bumpchart_df)
bumpchart_graph = bumpchart.create_bumpchart_graph(bumpchart_fig=bumpchart_fig)
bumpchart = bumpchart.create_bumpchart(
    bumpchart_ddm=bumpchart_ddm, 
    bumpchart_graph=bumpchart_graph
)

# Table
top_n = 5
year_min, year_max = preprocess_vsCommon.get_min_and_max_year(df=table_df)
table_range_slider = table.create_table_range_slider(year_min=year_min, year_max=year_max)
table_title = table.create_table_title(year_min_displayed=year_min, year_max_displayed=year_max, genre_displayed="All", top_n=top_n)
top_n_df, oldest_df, latest_df = table.query_data_for_table(table_df=table_df, genre="All", from_year=year_min, to_year=year_max, top_n=top_n)
table_top_n_fig, table_oldest_fig, table_latest_fig = table.create_table_fig(top_n_df=top_n_df, oldest_df=oldest_df, latest_df=latest_df, top_n=top_n)
table_top_n_graph = table.create_table_top_n_graph(table_top_n_fig=table_top_n_fig)
table_latest_graph = table.create_table_latest_graph(table_latest_fig=table_latest_fig)
table_oldest_graph = table.create_table_oldest_graph(table_oldest_fig=table_oldest_fig)
table_slider = table.create_table_slider(initial_value=top_n)
              
# Bar Chart
barchart_fig = barchart.create_barchart_fig(barchart_df=barchart_df)
barchart_graph = barchart.create_barchart_graph(barchart_fig=barchart_fig)
barchart_table_fig = barchart.create_empty_table_fig(distinction_df=distinction_df)
barchart_table_graph = barchart.create_barchart_table_graph(barchart_table_fig=barchart_table_fig)
barchart = barchart.create_barchart(
    barchart_graph=barchart_graph, 
    barchart_table_graph=barchart_table_graph
)

# Horizontal Bar Chart
h_barchart_ddm = hbarchart.create_h_barchart_dropdown_menu(h_barchart_df=h_barchart_df)
h_barchart_fig = hbarchart.create_h_barchart_fig(producer="Étienne Desrosiers", h_barchart_df=h_barchart_df, avg_df=avg_df)
h_barchart_graph = hbarchart.create_h_barchart_graph(h_barchart_fig=h_barchart_fig)
h_barchart = hbarchart.create_h_barchart(h_barchart_graph=h_barchart_graph, h_barchart_ddm=h_barchart_ddm)

# Create dashboard
app.layout = html.Div(children=[
    # Header
    html.Div([
        html.H2("Projet Cinémathèque québécoise", id='header-H2'),
        html.A(href="#sunburst", children=[
            html.H3('>> COMMENCER <<', id='link-header'),
            ]
        )
    ],className='header'),
    # VIZ 1 - Sunburst
    html.Div(id='sunburst', className='part-div-2', children=[
        html.H3(className='title-div', children=['HIÉRARCHIE DES DIFFÉRENTS GENRES CINÉMATOGRAPHIQUES']),
        html.Div(className='two-blocks-div', children=[
            html.Div(className='text-div-1', children=[
                html.P(className='text-p', children=[
                    "Le catalogue de la Cinémathèque québécoise regroupe un grand nombre de productions \
                    dont chacune possède ses spécificités et son genre cinématographique. \
                    La visualisation ci-contre a donc pour but de vous permettre de plonger au coeur \
                    de la diversité des oeuvres de la Cinémathèque. Les oeuvres ont été regroupées en 12 genres \
                    majeurs puis en sous-genres. Cela permet également de mettre en avant les genres d\'oeuvres \
                    qui sont le plus présentes dans le catalogue : les oeuvres Documentaires et Autres. Le genre \
                    'Autres' regroupe notamment les oeuvres indépendantes.",
                    html.Br(),
                    "A l\'aide de votre souris, vous pouvez intéragir avec le graphique en cliquant ou passant \
                    votre souris dessus afin d'obtenir plus d'informations.*"
                    ]),
                html.P(className='text-p text-italic', children=[
                    "* Certaines oeuvres de la base de données n'avaient pas de genre attribué \
                    et ont été regroupées dans la catégorie 'n.d'. Cette catégorie n'est pas représentée sur\
                    cette visualisation."
                    ]),
                ]),
            
            html.Div(className='viz-div', children=[
                sunburst
                ]),
        ]),
    ]),

    # VIZ 2 - Bumpchart
    html.Div(className='part-div-1', children=[
        html.H3(className='title-div', children=['CLASSEMENT DES GENRES AU COURS DU TEMPS']),
        html.Div(className='two-blocks-div', children=[
            html.Div(className='text-div-3', children=[
                html.P(className='text-p', children=[
                    'L’industrie du cinéma est très dynamique ce qui rend son évolution parfois complexe \
                    à appréhender. A travers cette visualisation, nous proposons de facilement \
                    retracer le classement des principaux genres en terme de nombres d’œuvres \
                    cinématographiques au cours du temps. On visualise ainsi la tendance générale qui \
                    montre que les documentaires et les films d’animation sont les genres ayant le plus de \
                    productions depuis 1910.',
                    html.Br(),
                    'Afin de comprendre et d’analyser plus finement le classement établi, le nombre de \
                    films produits pour une année donnée est affiché lorsque le curseur de la souris est \
                    placé sur le graphique.\
                    Enfin, il est également possible de sélectionner un genre en particulier grâce au menu \
                    déroulant et des informations complémentaires sont à disposition dans les tableaux ci-dessous.'
                    ]),
                html.P(className='text-p text-italic', children=[
                    "* La catégorie 'n.d', pour 'non déterminé', regroupe l'ensemble des films n'ayant pas de genre\
                        attribué dans la base de donnée."
                    ]),
                ]),
            
            html.Div(className='viz-div graph-div', children=[
                bumpchart
            ]),
        ]),
    # VIZ 3 - TABLE
        html.Div(className="table-div", children=[
            html.Div(className='text-div-2', children=[
                html.Div(children=[
                        table_title,
                        html.P('Sélectionner une période de temps', className='table-option-title'),
                        table_range_slider,
                        html.P('Sélectionner le TOP N des langues les plus utilisées', className='table-option-title'),
                        table_slider,
                ]),
            ]),

            html.Div(className='table-container',children=[
                html.Div(className='first-table',children=[
                    table_top_n_graph, 
                ]),
                html.Div(className='second-table',children=[
                    table_latest_graph, 
                ]),
                html.Div(className='third-table',children=[
                    table_oldest_graph, 
                ]),
            ])
        ])
    ],style={'height':'1200px'}),
    # VIZ 4 - Treemap
    html.Div(className='part-div-2', children=[
        html.H3(className='title-div', children=['COMPARAISON GÉOGRAPHIQUE DES DIFFÉRENTS GENRES CINÉMATOGRAPHIQUES']),
        html.Div(className='two-blocks-div', children=[
            html.Div(className='text-div-1', children=[
                html.P(className='text-p', children=[
                    "Le catalogue de la Cinémathèque québecoise dispose d'oeuvres du monde entier.\
                    A l\'aide de la visualisation ci-contre, vous pouvez voir les pays qui produisent le plus\
                    de films selon les continents. On remarque ainsi que les oeuvres provenant États-Unis, le Canada \
                    et la France sont celles les plus présentes dans le catalogue de la Cinémathèque.",
                    html.Br(),
                    "Il vous est possible d\'intéragir avec la visualisation en cliquant dessus mais aussi \
                    en filtrant sur un genre en particulier et sélectionner une période de temps entre 1901 et 2019."
                    ])
                ]),
            
            html.Div(className='viz-div graph-div', children=[
                treemap
            ]),
        ]),
    ]),

    # VIZ 5 - Barchart
    html.Div(className='part-div-1', children=[
        html.H3(className='title-div', children=['LES GENRES EXPLORÉS PAR UN RÉALISATEUR']),
        html.Div(className='two-blocks-div', children=[
            html.Div(className='text-div-1', children=[
                html.P(className='text-p', children=[
                    "Bien souvent, un réalisateur ne se limite pas à un seul genre au cours de sa carrière.\
                    Quand certains restent sur un genre qu'ils maîtrisent, d'autres expérimentent et tentent \
                    de nouvelles choses. C'est un choix qui leur revient et peut s'expliquer par leurs intérêts,\
                    leurs goûts et l'avancée dans leurs carrières.", 
                    html.Br(),
                    "Cette visualisation montre donc les genres explorés par un réalisateur donné en comparaison \
                    avec la moyenne de tous les réalisateurs confondus.*"
                    ]),
                 html.P(className='text-p text-italic', children=[
                    "* La catégorie 'n.d', pour 'non déterminé', regroupe l'ensemble des films n'ayant pas de genre\
                        attribué dans la base de donnée."
                    ]),
                ]),
            
            html.Div(className='viz-div graph-div', children=[
                h_barchart
            ]),
        ]),
    ]),
    # VIZ 6 - HISTOGRAM
    html.Div(className='part-div-2', children=[
            html.H3(className='title-div', children=['LES PERSONNALITÉS LES PLUS RÉCOMPENSÉES']),
            html.Div(className='text-div-2', children=[
                html.P(className='text-p', children=[
                    'Les efforts exceptionnels d’individus du milieu du cinéma ne passent pas toujours inaperçus. \
                En effet, certaines personnalités se voient remettre des distinctions prestigieuses \
                afin de récompenser leur talent et efforts. La prochaine et dernière visualisation présente les \
                distinctions remises à 159 personnalités du monde du cinéma, mais aussi de la \
                musique. Un ensemble de 855 distinctions différentes remises entre 1839 et 2021 sont\
                illustrées à l\'aide d’une visualisation intéractive. Un histogramme présente la distribution du\
                nombre de distinctions total reçu pour chaque individu, et un simple clic permet de \
                présenter de l\'information additionelle sur l\'individu choisi.'
                    ]),
                ]),
            
            html.Div(className='distinction-container', children=
                barchart
            )
        
    ]),

    html.Div([
        html.H3("Polytechnique Montréal - INF8808 H21 - Groupe 7", id='footer-H3'),
    ],className='footer'),

])
# Set callbacks
@app.callback([
               Output(component_id='treemap-title', component_property='children'),
               Output(component_id='treemap-graph', component_property='figure'),
               Output(component_id='bumpchart-graph', component_property='figure'),
               Output(component_id='table-title', component_property='children'),
               Output(component_id='table-top-n-graph', component_property='figure'),
               Output(component_id='table-latest-graph', component_property='figure'),
               Output(component_id='table-oldest-graph', component_property='figure'),
               Output(component_id='barchart-table-graph', component_property='figure'),
               Output(component_id='h-barchart-graph', component_property='figure')],
              [Input(component_id='treemap-dropdown-menu', component_property='value'),
               Input(component_id='treemap-range-slider', component_property='value'),
               Input(component_id='bumpchart-dropdown-menu', component_property='value'),
               Input(component_id='table-range-slider', component_property='value'),
               Input(component_id='table-slider', component_property='value'),     
               Input(component_id='barchart-graph', component_property='clickData'),
               Input(component_id='hbarchart-dropdown-menu', component_property='value')])
def update_viz(treemap_ddm_value, treemap_rs_values, bumpchart_ddm_value, table_rs_values, table_s_value, barchart_click,hbarchart_ddm_value):     
    # Sunburst
    # No callback

    # Treemap 
    treemap_title, treemap_fig = callback.callback_treemap(
        treemap_df=treemap_df,
        slider_min_year=treemap_rs_values[0], 
        slider_max_year=treemap_rs_values[1], 
        ddm_genre=treemap_ddm_value
    )

    # Bumpchart
    bumpchart_fig = callback.callback_bumpchart(
        bumpchart_df=bumpchart_df, 
        ddm_genre=bumpchart_ddm_value
    )

    # Table
    table_title, table_top_n_fig, table_latest_fig, table_oldest_fig = callback.callback_table(
        table_df=table_df,
        slider_min_year=table_rs_values[0], 
        slider_max_year=table_rs_values[1], 
        ddm_genre=bumpchart_ddm_value,
        top_n=table_s_value[0] 
    )

    # Barchart
    barchart_table_fig = callback.callback_barchart(
        distinction_df=distinction_df, 
        barchart_click=barchart_click
    )

    # Horizontal bar chart
    hbarchart_fig = callback.callback_hbarchart(hbarchart_ddm_value, h_barchart_df, avg_df)
    
    return treemap_title, treemap_fig, bumpchart_fig, table_title, table_top_n_fig, table_latest_fig, table_oldest_fig, barchart_table_fig, hbarchart_fig