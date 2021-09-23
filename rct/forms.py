from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LocationFormAdd(FlaskForm):
    small_location = StringField("small_location ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Добавить")