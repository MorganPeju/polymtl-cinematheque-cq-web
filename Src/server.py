#
# This file contains the functions relative to the Dash app server.
#


# External lib
from flask_failsafe import failsafe


# Local lib
# none


@failsafe
def create_app():
    """
    Gets the underlying Flask server from a new Dash app.

    Parameters
    ----------
    -

    Raises
    ------
    -

    Returns
    -------
    app : dash.app.server()
        The dash app's server

    Sources
    -------
    -

    See Also
    --------
    -
    """

    # the import is intentionally inside to work with the server failsafe - see tp5
    from app import app  # pylint: disable=import-outside-toplevel

    return app.server


if __name__ == "__main__":
    create_app().run(port="8040", debug=True)
