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
