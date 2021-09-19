from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms import validators
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you:',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
  author = StringField(' author:',validators=[Required()])
  category = SelectField("Choose your desired category:",choices=[('Experience','Experience'),('Technology','Technology'),('Education','Education'),('Humour','Humour'),('Intelligence','Intelligence')])
  pitch = TextAreaField('Add text here:',validators=[Required()])
  submit = SubmitField('Submit')


class CommentForm(FlaskForm):
  comment = TextAreaField('Add a Comment:',validators=[Required()])
  submit = SubmitField('Submit')     