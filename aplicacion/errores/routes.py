from flask import render_template
from . import errores


@errores.app_errorhandler(404)
def page_not_found(error):
    return (render_template("error.html", error="Página no encontrada..."),404)
@errores.app_errorhandler(403)
def forbidden(err):
    return (render_template("unforbidden.html"),403)
    