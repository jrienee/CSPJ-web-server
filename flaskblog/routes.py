from flaskblog import app, db, mail
from flask import Flask, render_template, url_for, flash, redirect, request
# from flaskblog.forms import *
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os, sqlite3
from PIL import Image
from flask_mail import Message
# from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, Form
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from wtforms.fields import EmailField, DateField
import hashlib

from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# conn = sqlite3.connect('user.db')
# c = conn.cursor()
# # # to create a users table (cannot create again if alr exists)
# c.execute("""CREATE TABLE users (
#             username text,
#             email text,
#             phone text,
#             birthdate text,
#             gender text,
#             password text
# )""")
# conn.commit()
# conn.close()

# class RegistrationForm(FlaskForm):
class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    # phone = StringField('Contact Number', validators=[DataRequired()])
    # birthdate = DateField('Birth Date', validators=[DataRequired()])
    # gender = SelectField('Gender', validators=[DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # def validate_phone(self, phone):
    #     conn = sqlite3.connect('user.db')
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM users WHERE phone='{}'".format(phone.data))
    #     user = c.fetchall()
    #     conn.commit()
    #     conn.close()
    #     if user:
    #         raise ValidationError('That phone number is taken. Please use a different one.')


    def validate_username(self,username):
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username='{}'".format(username.data))
        user = c.fetchall()
        conn.commit()
        conn.close()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email='{}'".format(email.data))
        user = c.fetchall()
        conn.commit()
        conn.close()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(Form):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=['POST','GET'])
@app.route("/home", methods=['GET'])
def home():
    form = SearchForm(request.form)
    if form.validate():
        print('hi submitted')
        conn = sqlite3.connect('site.db')
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM post WHERE title='{}'".format(form.searched.data))
            # user = c.fetchall()
        except:
            c.executescript("SELECT * FROM post WHERE title='{}'".format(form.searched.data))
            # user = c.fetchall()
        finally:
            posts = c.fetchall()
            conn.commit()
            conn.close()
            print(posts)
    else:
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        c.execute("SELECT * FROM post")
        # user = c.fetchall()

        posts = c.fetchall()
        conn.commit()
        conn.close()
        print(posts)
        if posts == []:
            posts = None
    return render_template("home.html", form=form, posts=posts)
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# @app.route("/search", methods=['GET'])
# def search():
#     form = SearchForm()
#     args = request.args
#     return args
#     # post=None
#     # if form.validate():
#     #     print('hi submitted')
#     #     conn = sqlite3.connect('site.db')
#     #     c = conn.cursor()
#     #     c.execute("SELECT * FROM post WHERE title='{}'".format(form.searched.data))
#     #     # user = c.fetchall()
#     #
#     #     post = c.fetchone()
#     #     conn.commit()
#     #     conn.close()
#     #     print(post)
#     return render_template("search.html", form=form,post=post)
#     return render_template("search.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    if form.validate():
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        pw = hashlib.md5(form.password.data.encode()).hexdigest()
        username = form.username.data
        email = form.email.data
        # phone = form.phone.data
        # birthdate = form.birthdate.data
        # gender = form.gender.data
        # c.execute("INSERT INTO users VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(username, email, phone, birthdate, gender, pw))
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, pw))
        conn.commit()
        conn.close()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if form.validate() and request.method == 'POST':
        # user = User.query.filter_by(email=form.email.data).first()
        conn = sqlite3.connect('site.db')
        c = conn.cursor()
        print(form.username.data)
        print(hashlib.md5(form.password.data.encode()).hexdigest())
        c.execute("SELECT * FROM users WHERE username='{}' AND password='{}'".format(form.username.data, hashlib.md5(form.password.data.encode()).hexdigest()))
        # user = c.fetchall()

        user = c.fetchone()
        conn.commit()
        conn.close()
        print(user)
        if user:
            # return redirect(url_for('login_success', users=user))

            return render_template('login_success.html', title='Login Success', users=user)
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/login_success")
def login_success(users):
    # username = current_user.username
    # email = current_user.email
    users = users.decode('utf8')
    return render_template('login_success.html', title='Login Success', users=users)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
def account():
    return redirect(url_for('home'))



# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         pw = form.password.data
#         username = form.username.data
#         email = form.email.data
#         phone = form.phone.data
#         birthdate = form.birthdate.data
#         gender = form.gender.data
#         user = User(username=username, email=email, phone=phone, birthdate=birthdate, gender=gender, password=pw)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         input_pw = form.password.data
#         pw = user.password
#         if user and (input_pw==pw):
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)#
# def save_pfp(form_pfp):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_pfp.filename)
#     pfp_fn = random_hex + f_ext
#     pfp_path = os.path.join(app.root_path, 'static/profile_pics', pfp_fn)
#     output_size = (125, 125)
#     i = Image.open(form_pfp)
#     i.thumbnail(output_size)
#     i.save(pfp_path)
#     return pfp_fn
#
# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.pfp.data:
#             pfp_file = save_pfp(form.pfp.data)
#             current_user.pfp_file = pfp_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         current_user.address = form.address.data
#         current_user.phone = form.phone.data
#         current_user.gender = form.gender.data
#         db.session.commit()
#         flash('Your account has been updated successfully!', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#         form.address.data = current_user.address
#         form.phone.data = current_user.phone
#         form.birthdate.data = current_user.birthdate
#         form.gender.data = current_user.gender
#     image_file = url_for('static', filename=f'profile_pics/{current_user.pfp_file}')
#     return render_template('account.html', title='Account', image_file=image_file, form=form)
#
# def send_reset_email(user):
#      token = user.get_reset_token()
#      msg = Message('Password Reset Request', sender='aspj.ecommerce.review@gmail.com', recipients=[user.email])
#      msg.body = '''To reset your password, visit the following link:
# {}
#
# If you did not make this request, please ignore this email and no changes would be made.
#      '''.format(url_for('reset_token', token=token, _external=True))
#      mail.send(msg)
#
# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)
#
# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ChangePasswordForm()
#     if form.validate_on_submit():
#         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_pw
#         db.session.commit()
#         flash('Your password has been changed successfully! You Are Now Able To Log In!', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)
#
# @app.route("/change_password", methods=['GET', 'POST'])
# @login_required
# def change_password():
#     pass
#
# @app.route("/delete_account", methods=['GET', 'POST'])
# @login_required
# def delete_account():
#     pass
