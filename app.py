from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination
from wtforms import StringField, IntegerField, SelectField, validators
from wtforms.validators import Length
from queryForm import query_form
from queryDropDowns import query_drop_downs
from datetime import datetime
from os import environ
from psycopg2 import OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)


class FilterForm(FlaskForm):
    # set up the form and grabbing drop downs, a dictionary of unique values to populate select fields
    drop_downs = query_drop_downs()

    year = datetime.now().year

    location = StringField("City, State", validators=[Length(max=60)])
    manufacturer = SelectField("Manufacturer", choices=drop_downs["manufacturer"], validators=[validators.optional()])
    model = StringField("Model", validators=[Length(max=40)])
    condition = SelectField("Condition", choices=drop_downs["condition"], validators=[validators.optional()])
    cylinders = SelectField("Cylinders", choices=drop_downs["cylinders"], validators=[validators.optional()])
    fuel = SelectField("Fuel", choices=drop_downs["fuel"], validators=[validators.optional()])
    transmission = SelectField("Transmission", choices=drop_downs["transmission"], validators=[validators.optional()])
    title_status = SelectField("Title Status", choices=drop_downs["title_status"], validators=[validators.optional()])
    vin = StringField("VIN", validators=[Length(max=40)])
    drive = SelectField("Drive", choices=drop_downs["drive"], validators=[validators.optional()])
    size = SelectField("Size", choices=drop_downs["size"], validators=[validators.optional()])
    vehicle_type = SelectField("Vehicle Type", choices=drop_downs["vehicle_type"], validators=[validators.optional()])
    paint_color = SelectField("Paint Color", choices=drop_downs["paint_color"], validators=[validators.optional()])
    price_start = IntegerField("Minimum Price", validators=[validators.optional(),
                                                            validators.NumberRange(min=0, max=10000000,
                                                                                   message="Please enter a value "
                                                                                           "between 0 and 10,000,000")])
    price_end = IntegerField("Maximum Price", validators=[validators.optional(),
                                                          validators.NumberRange(min=0, max=10000000,
                                                                                 message="Please enter a value between "
                                                                                         "0 and 10,000,000")])
    year_start = IntegerField("Minimum Year", validators=[validators.optional(),
                                                          validators.NumberRange(min=1880, max=year + 1,
                                                                                 message=f"Please enter a year between "
                                                                                         f"1880 and {year + 1}")])
    year_end = IntegerField("Maximum Year", validators=[validators.optional(),
                                                        validators.NumberRange(min=1880, max=year + 1,
                                                                               message="Please enter a year between "
                                                                                       f"1880 and {year + 1}")])
    odometer_start = IntegerField("Minimum Odometer", validators=[validators.optional(),
                                                                  validators.NumberRange(min=0, max=10000000,
                                                                                         message="Please enter a value "
                                                                                                 "between 0 and 10,"
                                                                                                 "000,000")])
    odometer_end = IntegerField("Maximum Odometer", validators=[validators.optional(),
                                                                validators.NumberRange(min=0, max=100000000,
                                                                                       message="Please enter a value "
                                                                                               "between 0 and 10,000,"
                                                                                               "000")])
    sort_by = SelectField("Sort By", choices=drop_downs["sort_by"], validators=[validators.optional()])


@app.route('/', methods=['GET', 'POST'])
def index():
    # render index.html with form passed through as a variable
    form = FilterForm()
    # validate_on_submit() runs when the form is submitted. we then redirect to search.html with the data fetched
    # from queryForm.py
    if form.is_submitted():
        session['form'] = form.data
        return redirect(url_for("search"))
    return render_template("index.html", form=form, success=True)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form_data = session['form']
    page = int(request.args.get('page', 1))
    per_page = 100
    offset = (page - 1) * per_page

    try:
        data, total_results = query_form(form_data, per_page, offset)
    except OperationalError as e:
        print(f"Critical database error: {e}")
        return render_template("error.html")
    if len(data) != 0:
        vehicle_pagination = Pagination(page=page,
                                        per_page=per_page,
                                        total=total_results,
                                        css_framework='bootstrap4')
        return render_template("search.html",
                               data=data,
                               page=page,
                               per_page=per_page,
                               total=total_results,
                               pagination=vehicle_pagination
                               )
    else:
        form = FilterForm()
        return render_template("index.html", form=form, success=False)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
