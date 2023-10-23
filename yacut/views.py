from flask import render_template, flash, redirect, abort
from sqlalchemy.exc import IntegrityError

from . import app
from .forms import URLForm
from .services import URL


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            short_link = URL(
                url=form.original_link.data, custom_id=form.custom_id.data
            ).get_short_link()
        except IntegrityError:
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'already_exists',
            )
            return render_template('yacut.html', form=form)
        flash(short_link, 'new_url')
        return render_template('yacut.html', form=form)
    return render_template('yacut.html', form=form)


@app.route('/<id>')
def redirect_view(id):
    url_object = URL().get_url(id)
    if not url_object:
        abort(404)
    return redirect(url_object.original)
