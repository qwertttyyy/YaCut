from flask import render_template, flash, redirect, abort

from . import app
from .forms import URLForm
from .services import URL


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        data = URL(form).get_data()
        if data.custom_id:
            if data.get_url():
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'already_exists',
                )
                return render_template('yacut.html', form=form)
        flash(data.get_short_link(), 'new_url')
        return render_template('yacut.html', form=form)
    return render_template('yacut.html', form=form)


@app.route('/<id>')
def redirect_view(id):
    url_object = URL().get_url(id)
    if url_object:
        return redirect(url_object.original)
    abort(404)
