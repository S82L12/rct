from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LocationFormAdd(FlaskForm):
    small_location = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Добавить")


class ModelFormAdd(FlaskForm):
    model = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField("Добавить")

class DeviceFormAdd(FlaskForm):
    id_aiu = StringField("id_aiu", validators=[DataRequired(), Length(4-10)])
    mac = StringField("mac", validators=[DataRequired()])
    ip = StringField("ip", validators=[DataRequired()])
    mask = StringField("mask", validators=[DataRequired()])
    docs = StringField("path")
    submit = SubmitField("Добавить")

