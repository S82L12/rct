from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, regexp, mac_address, ip_address
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField



class LocationFormAdd(FlaskForm):
    small_location = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Добавить")


class ModelFormAdd(FlaskForm):
    model = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Добавить")

