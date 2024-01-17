from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
class Formulariologin(FlaskForm): 
    usuariologin = StringField("Usuario", validators=[DataRequired("Ingrese su usuario")])
    contraseñalogin = PasswordField("Contraseña", validators=[DataRequired("Ingrese su contraseña")])
    submitlogin = SubmitField('Iniciar Sesión')

class Formularioregistro(FlaskForm): 
    usuarioreg = StringField("Usuario", validators=[DataRequired("Ingrese su usuario")])
    correoreg = StringField("Correo electrónico", validators=[DataRequired("Ingrese su correo electrónico"), Email(message="Ingrese un correo válido")])
    contraseñareg = PasswordField("Contraseña", validators=[DataRequired("Ingrese su contraseña")])
    submitreg = SubmitField('Registrarse')