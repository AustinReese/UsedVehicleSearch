from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, IntegerField, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired
from queryForm import queryForm
from queryDropdowns import queryDropdowns
from datetime import datetime
from os import environ


app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)

class FilterForm(FlaskForm):
    #set up the form and grabbing dropdowns, a dictionary of unique values to populate select fields
    DROPDOWNS = queryDropdowns()
    
    year = datetime.now().year
    
    location = StringField("City, State", validators = [Length(max=60)])
    manufacturer = SelectField("Manufacturer", choices = DROPDOWNS["manufacturer"], validators = [validators.optional()])    
    model = StringField("Model", validators = [Length(max=40)])
    condition = SelectField("Condition", choices = DROPDOWNS["condition"], validators = [validators.optional()])    
    cylinders = SelectField("Cylinders", choices = DROPDOWNS["cylinders"], validators = [validators.optional()])
    fuel = SelectField("Fuel", choices = DROPDOWNS["fuel"], validators = [validators.optional()])
    transmission = SelectField("Transmission", choices = DROPDOWNS["transmission"], validators = [validators.optional()])
    titleStatus = SelectField("Title Status", choices = DROPDOWNS["titleStatus"], validators = [validators.optional()])
    vin = StringField("VIN", validators = [Length(max=40)])
    drive = SelectField("Drive", choices = DROPDOWNS["drive"], validators = [validators.optional()])
    size = SelectField("Size", choices = DROPDOWNS["size"], validators = [validators.optional()])
    vehicleType = SelectField("Vehicle Type", choices = DROPDOWNS["vehicleType"], validators = [validators.optional()])
    paintColor = SelectField("Paint Color", choices = DROPDOWNS["paintColor"], validators = [validators.optional()])
    priceStart = IntegerField("Minimum Price", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])
    priceEnd = IntegerField("Maximum Price", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])    
    yearStart = IntegerField("Minimum Year", validators=[validators.optional(), validators.NumberRange(min=1880, max=year + 1, message="Please enter a year between 1880 and {}".format(year + 1))])
    yearEnd = IntegerField("Maximum Year", validators=[validators.optional(), validators.NumberRange(min=1880, max=year + 1, message="Please enter a year between 1880 and {}".format(year + 1))])
    odometerStart = IntegerField("Minimum Odometer", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])
    odometerEnd = IntegerField("Maximum Odometer", validators=[validators.optional(), validators.NumberRange(min=0, max=100000000, message="Please enter a value between 0 and 10,000,000")])
    sortBy = SelectField("Sort By", choices = DROPDOWNS["sortBy"], validators = [validators.optional()])

@app.route('/', methods=['GET', 'POST'])
def index():
    #render index.html with form passed through as a variable
    form = FilterForm()
    #validate_on_submit() runs when the form is submitted. we then redirect to search.html with the data fetched from queryForm.py
    success = True
    if form.is_submitted():
        data = queryForm(form)
        if len(data) != 0:
            return render_template("search.html", data = data)
        else:
            success = False
    return render_template("index.html", form = form, success = success)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
