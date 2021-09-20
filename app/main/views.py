from flask import render_template, request, redirect, url_for, abort
from flask.helpers import flash
from . import main
from .forms import UpdateProfile
from ..models import User
from flask_login import login_required
from .. import db,photos
from flask_login import login_required, current_user
# import markdown2  
from .forms import PostForm, CommentForm, UpdateProfile
from ..models import Post, Comment, User, Upvote, Downvote


@main.route('/')
def index():
    posts = Post.query.order_by(Post.added_date.desc()).all()
    fashion= Post.query.filter_by(category='fashion').all()
    sports = Post.query.filter_by(category='sports').all()
    business = Post.query.filter_by(category='Business').all()
    posts = Post.query.order_by(Post.added_date.desc()).all()
    return render_template('index.html', business=business, fashion=fashion, sports=sports, posts=posts)


@main.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('pitch.html', posts=posts, likes=likes, user=user)




@main.route("/user/<uname>")
@login_required
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route("/user/<uname>/update", methods=["GET", "POST"])
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for(".profile", uname=user.username))

    return render_template("profile/update.html", form=form)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



# @main.route('/user/<uname>/update',methods = ['GET','POST'])
# def update_profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)

#     form = UpdateProfile()

#     if form.validate_on_submit():
#         user.bio = form.bio.data

#         db.session.add(user)
#         db.session.commit()

#         return redirect(url_for('.profile',uname=user.username))

#     return render_template('profile/update.html',form =form)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        # post_obj = Post(post=post, title=title, category=category, user_id=user_id)
        new_post=Post(title=title,post=post,category=category)
        new_post.save()
        db.session.add(new_post)
        db.session.commit()
        # post_obj.save()
        flash('Your pitch has been created successfully!')
        return redirect(url_for('main.index',uname=current_user.username))
    return render_template('new_pitch.html', form=form ,title='Pitch Perfect')


@main.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    user = User.query.all()
    comments = Comment.query.filter_by(post_id=post_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            post_id=post_id,
            user_id=user_id
        )
        new_comment.save_comment()
        new_comments = [new_comment]
        print(new_comments)
        flash('Your comment has been created successfully!')
        return redirect(url_for('.comment', post_id=post_id))
    return render_template('comment.html', form=form, post=post, comments=comments, user=user)


@main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ('not found')
    return render_template('profile.html', user=user)





# @main.route('/user/<name>/update_profile', methods=['POST', 'GET'])
# @login_required
# def updateprofile(name):
#     form = UpdateProfile()
#     user = User.query.filter_by(username=name).first()
#     if user is None:
#         error = 'The user does not exist'
#     if form.validate_on_submit():
#         user.bio = form.bio.data
#         user.save()
#         return redirect(url_for('.profile', name=name))
#     return render_template('profile/update_profile.html', form=form)


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
        
    upvote= Upvote.query.filter_by(user_id=current_user.id, post_id=id).first()
    if upvote is not None:
        
        db.session.delete(upvote)
        db.session.commit()
        
        return redirect(url_for('.index'))
    
    new_like = Upvote(
        user_id=current_user.id,
        post_id=id
        
    )
    db.session.add(new_like)
    db.session.commit()

        
    return redirect(url_for('main.posts'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    post = Post.query.get(id)
    nv = Downvote(post=post, downvote=1)
    nv.save()
    return redirect(url_for('main.posts'))