import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination
from wtforms import StringField, IntegerField, SelectField, validators
from wtforms.validators import Length
from queryForm import query_filter_form, query_table_form
from queryDropDowns import query_drop_downs
from datetime import datetime
from os import environ
from psycopg2 import OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)

OFFLINE_DEBUG = False

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



class TableForm(FlaskForm):
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
    group_by = SelectField("Group By", choices=drop_downs["numerical_fields_backwards"], validators=[validators.data_required()])
    display_field = SelectField("Display Field", choices=drop_downs["numerical_fields"], validators=[validators.data_required()])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        session['form'] = filter_form.data
        return redirect(url_for("search"))
    return render_template("filter.html", form=filter_form, success=True)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form_data = session['form']
    page = int(request.args.get('page', 1))
    per_page = 100
    offset = (page - 1) * per_page

    try:
        data, total_results = query_filter_form(form_data, per_page, offset, offline_debug=OFFLINE_DEBUG)
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
        filter_form = FilterForm()
        return render_template("filter.html", form=filter_form, success=False)

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    table_form = TableForm()
    if table_form.validate_on_submit():
        try:
            if table_form.data["group_by"] == table_form.data["display_field"]:
                return render_template("tables.html",
                                       form=table_form,
                                       success="invalid_selection_failure",
                                       table=None,
                                       group_by=None,
                                       display=None,
                                       total_results=None)

            data, total_results, min_group_by = query_table_form(table_form.data, offline_debug=OFFLINE_DEBUG)
            group_by =  table_form.data["group_by"]
            display_field = table_form.data["display_field"]
        except OperationalError as e:
            print(f"Critical database error: {e}")
            return render_template("error.html")
        if len(data) != 0:
            pd_data = pd.DataFrame(data, columns=[display_field, group_by])
            group_by_quantiles = [0 if min_group_by == None else min_group_by]
            quantile_data = {"Percentiles": ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]}
            for i in range(10):
                group_by_quantiles.append(pd_data[group_by].quantile((i + 1) / 10))

            for i in range(10):
                group_by_quantiles_df = pd_data[pd_data[group_by].between(group_by_quantiles[i], group_by_quantiles[i + 1])]
                display_quantiles = [0]
                display_means = []
                for j in range(10):
                    display_quantiles.append(group_by_quantiles_df[display_field].quantile((j + 1) / 10))
                for j in range(10):
                    display_quantiles_df = group_by_quantiles_df[group_by_quantiles_df[display_field].between(display_quantiles[j], display_quantiles[j + 1])]
                    display_mean = display_quantiles_df[display_field].mean()
                    try:
                        if display_field == "price":
                            display_means.append(f"${int(display_mean):,}")
                        elif display_field == "year":
                            display_means.append(f"{int(display_mean)}")
                        else:
                            display_means.append(f"{int(display_mean):,}")
                    except:
                        display_means.append("No Info")
                if group_by == "price":
                    quantile_data[f"${int(group_by_quantiles[i]):,}-${int(group_by_quantiles[i + 1]):,}"] = display_means
                elif group_by == "year":
                    quantile_data[f"{int(group_by_quantiles[i])}-{int(group_by_quantiles[i + 1])}"] = display_means
                else:
                    quantile_data[f"{int(group_by_quantiles[i]):,}-{int(group_by_quantiles[i + 1]):,}"] = display_means

            percentile_html_list = pd.DataFrame(quantile_data).to_html(border=0, index=False).split("</thead>")
            percentile_html = percentile_html_list[0]\
                                .replace('''class="dataframe"''', '''class="table table-striped"''')\
                                .replace("<th>", '''<th scope="col">''')\
                                + "</thead>"\
                                + percentile_html_list[1]\
                                .replace("<th>", '''<th scope="row">''')

            return render_template("tables.html",
                                   form=table_form,
                                   success="success",
                                   table=percentile_html,
                                   group_by=group_by,
                                   display=display_field,
                                   total_results=f"{int(total_results):,}")
        else:
            return render_template("tables.html",
                                   form=table_form,
                                   success="no_data_failure",
                                   table=None,
                                   group_by=None,
                                   display=None,
                                   total_results=None)

    return render_template("tables.html",
                                   form=table_form,
                                   success="success",
                                   table=None,
                                   group_by=None,
                                   display=None,
                                   total_results=None)

@app.route('/tables_help')
def tables_help():
    return render_template("tables_help.html")

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
