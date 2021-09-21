from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug import generate_password_hash,check_password_hash
from datetime import datetime



    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    profile_pic_path = db.Column(db.String())
    bio = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
            self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    post = db.Column(db.String(255))
    category = db.Column(db.String(255))
    title = db.Column(db.String(255))
    vote_count = db.Column(db.Integer)
    added_date = db.Column(db.DateTime,default=datetime.utcnow)
    author = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    upvote = db.relationship('Upvote', backref='post', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='post', lazy='dynamic')
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"    
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text(), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Comment: {self.comment}'
    
    
    
class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key = True)
    upvote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
    def save_upvote(self):
        db.session.add(self)
        db.session.commit()
    def delete_upvote(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Upvote: {self.upvote}'
    
class Downvote(db.Model):
    __tablename__= 'downvotes'
    id = db.Column(db.Integer, primary_key = True)
    downvote = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    def save_downvote(self):
        db.session.add(self)
        db.session.commit()
    def delete_downvotevote(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Downvote: {self.downvote}'