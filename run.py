from aplicacion import app
from aplicacion.config.email import mail


if __name__ == '__main__':
    mail.init_app(app)
    app.run()
