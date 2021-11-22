from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, regexp, mac_address, ip_address
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField



class LocationFormAdd(FlaskForm):
    small_location = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=100)]) # название поля ввода = "small_location " name field input
    submit = SubmitField("Добавить")


class ModelFormAdd(FlaskForm):
    model = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Добавить")

class ModelswFormAdd(FlaskForm):
    modelsw = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Добавить")

class AddressSwitchAdd(FlaskForm):
    address = SelectField("address", choices=[])
    switch = SelectField("switch", choices=[])



