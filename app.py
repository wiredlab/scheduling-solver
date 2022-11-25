
import re
import csv
import os
import sys
from shutil import rmtree
from tempfile import mkdtemp
import time

from flask import Flask, redirect, request, render_template, make_response, session, url_for

from flask_wtf import FlaskForm, csrf
from flask_wtf.file import FileField, FileRequired

# from wtforms import IntegerField, RadioField, StringField
# from wtforms.validators import DataRequired, NumberRange, Optional

from werkzeug.utils import secure_filename

import schedulingLP


app = Flask(__name__)

app.config.update(
    DELETE_TEMP_FILES = True,
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024,
)

app.secret_key = 'foo'
# csrf.CSRFProtect(app)

KEEP_FILES = 'SCHEDULING_KEEP_FILES' in os.environ
# JPG_CACHE = os.environ.get('PHOTOROSTER_JPG_CACHE', os.path.join(os.getcwd(), 'cache'))

# app.debug = True


class SchedulingForm(FlaskForm):
    xlsxfile = FileField('XLSX file', [FileRequired()])



@app.route('/', methods=['GET', 'POST'])
def scheduling():
    form = SchedulingForm()

    if form.validate_on_submit():
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(time.time()))
        tmpdir = '/tmp/scheduling-app_%i' % (int(100*time.time()),)
        os.mkdir(tmpdir, mode=0o777)
        print(tmpdir)

        data = form.xlsxfile.data
        filename = form.xlsxfile.data.filename
        xlsxname = os.path.join(tmpdir, secure_filename(filename))
        form.xlsxfile.data.save(xlsxname)

        session['upload'] = (xlsxname, form.xlsxfile.data.filename, tmpdir)
        session['app'] = 'scheduling'
        # response = 'ok'
        print(f'Upload: {xlsxname}')
        response = redirect(url_for('result'))
        output, result = schedulingLP.run(xlsx_file=data)
        print(result)

        response = render_template('scheduling.html',
                                   form=form,
                                   filename=filename,
                                   timestamp=timestamp,
                                   output=output,
                                   result=result)
    else:
        if 'upload' in session:
            #cleanup stale session
            session.pop('upload', None)
            session.pop('app', None)

        response = render_template('scheduling.html', form=form)

    return response

@app.route('/result', methods=['GET', 'POST'])
def result():
    print('HERE')
    print(request.method)
    # return redirect(url_for('scheduling'))
    # return('<h1>Result</h1>')
    referrer = session.pop('app', None)
    (inpath, inname, tmpdir) = session.pop('upload', (None, None, None))

    missing_context = ((referrer is None), (inpath is None), (inname is None))

    if all(missing_context):
        # not sure how we got here
        return redirect(url_for('/'))
    elif any(missing_context):
        # anything missing is an application error
        raise TypeError(f'Incomplete session referrer: {referrer}, upload: ({inpath}, {inname})')

    # process the file according to the app
    try:
        if referrer == 'scheduling':
            output = schedulingLP.run(xlsx_file=inpath)
            response = make_response(output)
            # response.headers['Content-Type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename=output.txt'
            response.mimetype = 'text/plain'
            print('THERE')
        else:
            raise TypeError(f'Unknown referrer: {referrer}')
    except:
        raise


    if app.config['DELETE_TEMP_FILES']:
        rmtree(tmpdir)

    print(response)
    return response


if __name__ == '__main__':
    app.run(debug=True)

