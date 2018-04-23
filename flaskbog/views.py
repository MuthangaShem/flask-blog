from flaskblog import app, db, login_manager
from flask import render_template, request, flash, url_for, g, session, redirect
from form import LoginForm, PostForm, TagForm, SearchForm
from models import db, Admin, Tag, Post, Pagination
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import PER_PAGE, MAX_SEARCH_RESULTS
