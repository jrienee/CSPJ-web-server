from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
import sqlite3

posts = Blueprint('posts',__name__)

@posts.route('/post/new',methods = ['GET','POST'])
def new_post():
    form = PostForm(request.form)
    if request.method == 'POST':
        print("hi")
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        title = form.title.data
        content = form.content.data
        c.execute("INSERT INTO post VALUES (?, ?, ?, ?)", (1, title, content, 1))
        conn.commit()
        conn.close()
        flash(f'Post created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post = post)

@posts.route("/post/<int:post_id>/update", methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form  = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
    title = 'Update Post', form=form, legend = 'Update Post')

@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main_app.home'))

