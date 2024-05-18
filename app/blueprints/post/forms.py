from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired


class CommentForm(FlaskForm):
    commenttext = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')


class GuessForm(FlaskForm):
    guesstext = TextAreaField('Guess', validators=[DataRequired()])
    submit = SubmitField('Guess! If you were wrong...')


class ImageuploadForm(FlaskForm):
    postimage = FileField('image', validators=[FileRequired()])
    submit = SubmitField('Upload Image')
