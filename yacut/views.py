from random import choice
from string import ascii_letters, digits

from flask import render_template, flash, url_for, redirect, abort

from . import app, db
from .constants import ID_SIZE
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    chars = ascii_letters + digits
    id = ''.join(choice(chars) for _ in range(ID_SIZE))
    return id


def create_url(original_link, short_id):
    if not short_id:
        short_id = get_unique_short_id()
        while URLMap.query.filter_by(short=short_id).first():
            short_id = get_unique_short_id()
    new_url_object = URLMap(original=original_link, short=short_id)
    db.session.add(new_url_object)
    db.session.commit()
    short_link = url_for('redirect_view', id=short_id, _external=True)
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        short = None
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'already_exists',
                )
                return render_template('yacut.html', form=form)
            short = custom_id
        short_link = create_url(original_link, short)
        flash(short_link, 'new_url')
        return render_template('yacut.html', form=form)
    return render_template('yacut.html', form=form)


@app.route('/<id>')
def redirect_view(id):
    url_object = URLMap.query.filter_by(short=id).first()
    if url_object:
        return redirect(url_object.original)
    abort(404)
