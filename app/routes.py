from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.models import Posts, User
from .forms import EditProfileForm, LoginForm, NewPostForm, RegisterForm, EmptyForm


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New post created!', 'success')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title="Home", posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route("/create/post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post = request.form.get("post")
        user = User.query.filter_by(username=current_user.username).first_or_404()
        new_post = Posts(title="What's on your mind?", body=post, author=user)
        db.session.add(new_post)
        db.session.commit()
        flash("New post created!", "success")
    
    return redirect(url_for("profile", username=current_user.username))


@app.route("/profile/<username>")
@login_required
def profile(username):
    form = EmptyForm()
    
    user = User.query.filter_by(username=username).first_or_404()
    posts_verify=Posts.query.filter_by(author=user)
    aux = [post for post in posts_verify]


    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Posts.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('profile', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("profile.html", title="Profile", posts=posts.items, user=user, aux=aux, form=form, next_url=next_url, prev_url=prev_url)


@app.route("/edit/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        
        if form.password.data:
            current_user.password_hash(form.password.data)

        db.session.commit()
        
        flash('Your changes have been saved', 'success')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email

    return render_template("edit_profile.html", title="Edit profile", user=user, form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!', 'warning')
            return redirect(url_for('profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username), 'success')
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))
    

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username), 'warning')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username), 'success')
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/explore')
@login_required
def explore():
    form = NewPostForm()
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Home', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()