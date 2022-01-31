#
# This file contains the functions to create the lighter .csv files that might allow Heroku app to run.
#


# External lib
import pandas as pd


# Local lib
import preprocess_vsBackEnd
import preprocess_vsCommon
import preprocess_vsSunburst
import preprocess_vsTreemap
import preprocess_vsBumpChart
import preprocess_vsTable
import preprocess_vsBarChart
import preprocess_vsHBarChart

def create_data_files():
    # load data
    raw_film_df = preprocess_vsBackEnd.create_master_film_df()
    film_df = preprocess_vsBackEnd.clean_film_df_columns(raw_film_df=raw_film_df)
    #preprocess_vsBackEnd.create_file_from_df(df=film_df, file_name="film_vsMaitre.csv")

    # Sunburst
    #sunburst_df = preprocess_vsSunburst.clean_film_df_for_sunburst(film_df=film_df)
    #preprocess_vsBackEnd.create_file_from_df(df=sunburst_df, file_name="p_sunburst.csv")

    # Bump Chart
    raw_bumpchart_df = preprocess_vsBumpChart.clean_film_df_for_bumpchart(film_df=film_df)
    #bumpchart_df = preprocess_vsBumpChart.prepare_data_for_bumpchart(raw_bumpchart_df=raw_bumpchart_df)
    #preprocess_vsBackEnd.create_file_from_df(df=bumpchart_df, file_name="p_bumpchart.csv")
    
    # Treemap
    treemap_df = preprocess_vsTreemap.create_treemap_df(raw_bumpchart_df=raw_bumpchart_df)
    preprocess_vsBackEnd.create_file_from_df(df=treemap_df, file_name="p_treemap.csv")

    # Table
    #table_df = preprocess_vsTable.create_table_df(raw_bumpchart_df=raw_bumpchart_df)
    #preprocess_vsBackEnd.create_file_from_df(df=table_df, file_name="p_table.csv")

    # Barchart
    #raw_distinction_df = preprocess_vsBackEnd.backend_load_distinction()
    #distinction_df = preprocess_vsBarChart.clean_distinction_df(raw_distinction_df=raw_distinction_df)
    #preprocess_vsBackEnd.create_file_from_df(df=distinction_df, file_name="p_distinction.csv") 

    # Horizontal Bar Chart
    #raw_h_barchart_df = preprocess_vsHBarChart.clean_film_df_for_h_barchart(film_df=film_df)
    #h_barchart_df = preprocess_vsHBarChart.create_h_barchart_df(raw_h_barchart_df=raw_h_barchart_df)
    #avg_df = preprocess_vsHBarChart.create_average_df_for_h_barchart(h_barchart_df=h_barchart_df)
    #preprocess_vsBackEnd.create_file_from_df(df=h_barchart_df, file_name="p_h_barchart.csv")
    #preprocess_vsBackEnd.create_file_from_df(df=avg_df, file_name="p_avg.csv") 
    
    return
