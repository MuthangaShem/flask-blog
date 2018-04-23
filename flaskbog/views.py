from flaskblog import app, db, login_manager
from flask import render_template, request, flash, url_for, g, session, redirect
from form import LoginForm, PostForm, TagForm, SearchForm
from models import db, Admin, Tag, Post, Pagination
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import PER_PAGE, MAX_SEARCH_RESULTS


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/posts', defaults={'page': 1})
@app.route('/posts/page/<int:page>')
def posts(page):
    count = db.session.query(Post).count()
    offset = (page - 1) * PER_PAGE
    posts = Post.query.limit(PER_PAGE).offset(offset)

    if not posts and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('posts.html', pagination=pagination, posts=posts)


@login_manager.user_loader
def load_user(user):
    return Admin.query.get(user)


@app.before_request
def before_request():
    g.user = current_user
    g.search_form = SearchForm()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.admin)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    flash("Logout successfully")
    logout_user()
    return redirect(url_for("index"))


@app.route('/post/<int:id>')
def post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post.html', post=post)


@app.route('/addpost', methods=["GET", "POST"])
@login_required
def addpost():
    form = PostForm(csrf_enabled=False)
    form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
    if request.method == "POST":
        if form.validate() == False:
            return render_template('addpost.html', form=form)
        else:
            tags = [Tag.query.filter_by(id=tag_id).first() for tag_id in form.tag.data]
            post = Post(form.title.data, form.text.data, tags)
            db.session.add(post)
        db.session.commit()
        flash('Posted successfully')
        return render_template('index.html')
    return render_template("addpost.html", form=form)


@app.route('/editpost/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    if request.method == 'POST':
        form = PostForm()
        form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
        if form.validate() == False:
            return render_template('editpost.html', form=form)
        else:
            tags = [Tag.query.filter_by(id=tag_id).first() for tag_id in form.tag.data]
            post = Post.query.filter_by(id=id).first()
            post.title = form.title.data
            post.text = form.text.data
            post.tags = tags
            db.session.merge(post)
            db.session.commit()
            flash('Post updated successfully')
            return render_template('index.html')
    elif request.method == 'GET':
        post = Post.query.filter_by(id=id).first()
        form = PostForm(id=post.id, title=post.title, text=post.text)
        form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
        return render_template('editpost.html', post_id=post.id, form=form)
