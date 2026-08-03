from flask import flash, render_template, redirect

from . import app, db
from .forms import FileUploaderForm, LinkShrinkerForm
from .url_shrinker import get_unique_short_id
from .models import URLMap
from .yandex_disk import async_upload_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkShrinkerForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        try:
            if not custom_id:
                custom_id = get_unique_short_id()
            url = URLMap(
                original=form.original_link.data,
                short=custom_id,
            )
            db.session.add(url)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            flash(str(e))
            return render_template('index.html', form=form)
        return render_template('index.html', form=form, short=custom_id)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_view():
    form = FileUploaderForm()
    if form.validate_on_submit():
        urls = await async_upload_files(form.files.data)
        files_info = []
        for file, url in zip(form.files.data, urls):
            short_id = get_unique_short_id()
            urlmap = URLMap(
                original=url,
                short=short_id,
            )
            files_info.append({
                'short_url': short_id,
                'filename': file.filename,
            })
            db.session.add(urlmap)
        db.session.commit()
        return render_template(
            'files_upload.html', form=form, files_info=files_info)
    return render_template('files_upload.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original)