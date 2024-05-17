from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    commenttext = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')


class GuessForm(FlaskForm):
    guesstext = TextAreaField('Guess', validators=[DataRequired()])
    submit = SubmitField('Guess! If you were wrong...')
