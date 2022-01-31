# External lib
# none

# Local lib
# none


#
# This file contains the functions to provides the templates for the tooltips.
#

def example_function_declaration(currency_id):
    """
    Imports the foreign exchange spot rate (USD to ???)
    The .csv file of fx spots must be in the "Data" directory (folder)

    Parameters
    ----------
    currency_id : string
        The data frame of prices (levels) indexed by data

    Raises
    ------
    -

    Returns
    -------
    spot_rate_time_series : pd.DataFrame()
        The dataframe of specified spot exchange rate nominated in USD.
        If "ALL" is passed then the entire dataframe is returned.

    Sources
    -------
    -

    See Also
    --------
    -
    """

    # Import .csv to a data frame
    relative_path = "../../Data/"
    file_name = "dataFx_vsSpot.csv"
    file = relative_path + file_name
    df = pd.read_csv(file,
                     sep=',',
                     header=0,
                     index_col=0,
                     parse_dates=True,
                     infer_datetime_format=True)

