from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms import validators
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you:',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
  title = StringField(' title:',validators=[Required()]) 
  post = StringField(' post:',validators=[Required()]) 
  author = StringField(' author:',validators=[Required()])
  category = SelectField("Choose your desired category:",choices=[('Business','Business'),('Fashion','Fashion'),('Education','Education'),('Humour','Humour'),('Sports','Sports')])
#   pitch = TextAreaField('Add text here:',validators=[Required()])
  submit = SubmitField('Submit')


class CommentForm(FlaskForm):
  comment = TextAreaField('Add a Comment:',validators=[Required()])
  submit = SubmitField('Submit')     