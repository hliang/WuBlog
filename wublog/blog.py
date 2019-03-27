# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
from .models import db, Post
from .auth import login_required

bp = Blueprint("blog", __name__)


# A function to get the post.
# Both the update and delete views will need to fetch a post by id and check
# if the author matches the logged in user. To avoid duplicating code, you can
# write a function to get the post and call it from each view.
def get_post(post_id, check_author=True):
    post = Post.query.get(post_id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            post = Post(title=title,
                        body=body,
                        author_id=g.user.id,
                        username=g.user.username)
            # print("post.id=%d" % post.id)
            # print("post.created=%s" % post.created)
            db.session.add(post)
            db.session.commit()
    return render_template('blog/create.html')


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = get_post(post_id=post_id, check_author=True)
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        error = None

        if not new_title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = new_title
            post.body = new_body
            db.session.commit()
            # print("11111111111")
            return redirect(url_for('blog.index'))

    # print("222222222222")
    return render_template('blog/update.html', post=post)


@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    post = get_post(post_id=post_id, check_author=True)  ## filter by current user_id
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(post_id))
    else:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog.index'))


