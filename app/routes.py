from app import app, db
from app.models import User, Post
from flask_login import login_user,logout_user,login_required, current_user
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, AddproductForm, EditProfileForm, PostForm
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Is Live')
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template(
        'index.html',
        title='Index',
        form=form,
        posts=posts)

@app.route("/register" , methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, has been registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {form.username.data}')
        return redirect(url_for('home'))   
    return render_template('login.html', title='Login', form=form)

@app.route("/addproduct", methods=['GET', 'POST'])
@login_required
def addproduct():
    form = AddproductForm() 
    if form.validate_on_submit():
        flash(f'You have added {form.product_name.data}')
        return redirect(url_for('home'))
    return render_template('addproduct.html', title='addproduct', form=form)

@app.route('/<username>/profile', methods=['GET', 'POST'])
@login_required
def profile(username):
    """Profile page"""
    user = User.query.filter_by(username=username).first_or_404()
    posts = current_user.posts.all()
    return render_template('profile.html', title='Profile',user=user, posts=posts)

@app.route('/edit-profile',  methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit ():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit ()
        flash( 'Your changes have been saved.')
        return redirect (url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template ('edit_profile.html', title ='Edit Profile', form=form)