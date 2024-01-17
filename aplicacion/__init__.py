from flask import Flask, redirect, request, session, url_for
from flask_babel import Babel
from .catalogo import catalogo
from .inicio import inicio
from .carrito import carrito
from .cuenta import cuenta
from .errores import errores
from flask_babel import _

app = Flask(__name__)
app.secret_key="1234"
app.config.from_pyfile('config/configuracion.cfg')

babel = Babel(app)

app.config['LANGUAGES'] = ['es', 'en']
app.config['BABEL_DEFAULT_LOCALE'] = 'es'

def get_locale():
    return session.get('idioma', request.accept_languages.best_match(app.config['LANGUAGES']))

@app.route('/cambiar_idioma/<idioma>')
def cambiar_idioma(idioma):
    if idioma in app.config['LANGUAGES']:
        session['idioma'] = idioma
        print(session['idioma'])
    return redirect(request.referrer or url_for('inicio.inicio'))

babel.init_app(app, locale_selector=get_locale)


app.register_blueprint(catalogo)
app.register_blueprint(inicio)
app.register_blueprint(carrito)
app.register_blueprint(cuenta)
app.register_blueprint(errores)
