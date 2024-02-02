# -*- coding: utf-8 -*-

import os
import time

from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileField, FileRequired

import schedulingLP


app = Flask(__name__)
app.secret_key = "topsecretlol"
csrf = CSRFProtect(app)


class SchedulingForm(FlaskForm):
    xlsxfile = FileField("XLSX file", [FileRequired()])


@app.route("/", methods=["GET", "POST"])
def root():
    form = SchedulingForm()

    if form.validate_on_submit():
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime())

        # get the XLSX file's bytes
        data = form.xlsxfile.data

        # do the deed!
        status, result = schedulingLP.run(xlsx=data)

        # result dict structure, each key is the name of a prof:
        # {'profname':{'courses': {'course1': int,
        #                          'course2': int, ...},
        #              'TLC': float,
        #              'capacity': int, }
        # }

        # Create the results page, this time with the result data
        response = render_template(
            "scheduling.html.j2",
            form=form,
            filename=form.xlsxfile.data.filename,
            timestamp=timestamp,
            status=status,
            result=result,
        )

    else:
        # invalid submission or fresh reloaded page
        response = render_template("scheduling.html.j2", form=form)

    return response


if __name__ == "__main__":
    app.run(debug=True)
