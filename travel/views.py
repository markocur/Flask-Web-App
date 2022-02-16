from flask import flash, redirect, render_template, request, url_for, abort
from travel import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from travel.helpers import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, User, Post
from flask_login import login_user, current_user, logout_user, login_required

#################################################
## routes accessible without login requirement ##
#################################################

@app.route("/home")
@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data) # creating password hash
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit() # commiting database changes and adding new user to the database
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() # creating instance of LoginForm class from helpers.py
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # finding user data in database
        if user and check_password_hash(user.password, form.password.data): # checking password
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

###################################
## routes with login requirement ##
###################################

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/journal")
@login_required
def journal():
    # query below allows me to display only the journal entries created by currently logged in user
    posts = Post.query.order_by(Post.date_posted.desc()).filter_by(author=current_user)
    return render_template("journal.html", posts=posts)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        current_user.password = hashed
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have added a new journal entry!', 'success')
        return redirect(url_for('journal'))
    return render_template("create_post.html", form=form, legend='Add New Journal Entry')

# Flask allows to use variables within routes,
# so here I am using post_id to create a route displaying a specific post/journal entry
@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # only the posts written by currently logged in user are accessible
        abort(403)
    return render_template('post.html', post=post)

# This is a route for updating journal entries
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # get_or_404 = Like get() but aborts with 404 if not found instead of returning None.
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # don't have to use db.session.add like before,
        # as we are just updating the content that already exists in the database
        db.session.commit() 
        flash('You have updated your journal entry!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form=form, title="Update Entry", legend="Update Journal Entry")


# This is a route for deleting journal entries
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your journal entry has been permanently deleted!', 'success')
    return redirect(url_for('journal'))