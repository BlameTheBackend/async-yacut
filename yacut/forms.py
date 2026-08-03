from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, URL


class LinkShrinkerForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, 16)]
    )
    submit = SubmitField('Создать')


class FileUploaderForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
