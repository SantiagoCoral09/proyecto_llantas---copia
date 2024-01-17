from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields import SelectField

class FormularioCompra(FlaskForm): 
    celular = StringField("Celular", validators=[DataRequired("Ingrese su número de celular")])
    direccion = StringField("Dirección de envío", validators=[DataRequired("Ingrese su dirección")])
    pago_opciones = [('pse', 'PSE'), ('tarjeta', 'Tarjeta de crédito'), ('efectivo', 'Efectivo')]
    pago = SelectField("Forma de Pago", choices=pago_opciones, validators=[DataRequired("Seleccione una forma de pago")])
    submit = SubmitField('Comprar')