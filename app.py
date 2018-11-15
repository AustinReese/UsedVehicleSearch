from errHandle import errHandle

errHandle()

#this is where the magic happens, we currently have only one route but that will change

from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, IntegerField, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired
from queryForm import queryForm
from queryDropdowns import queryDropdowns
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)


class FilterForm(FlaskForm):
    #set up the form and grabbing dropdowns, a dictionary of unique values to populate select fields
    dropdowns = queryDropdowns()
    
    year = datetime.now().year
    
    city = StringField("City", validators = [Length(max=40)])
    state = SelectField("State", choices = dropdowns["states"], validators = [validators.optional()])
    manufacturer = SelectField("Manufacturer", choices = dropdowns["manufacturer"], validators = [validators.optional()])    
    make = StringField("Make", validators = [Length(max=40)])
    condition = SelectField("Condition", choices = dropdowns["condition"], validators = [validators.optional()])    
    cylinders = SelectField("Cylinders", choices = dropdowns["cylinders"], validators = [validators.optional()])
    fuel = SelectField("Fuel", choices = dropdowns["fuel"], validators = [validators.optional()])
    transmission = SelectField("Transmission", choices = dropdowns["transmission"], validators = [validators.optional()])
    titleStatus = SelectField("Title Status", choices = dropdowns["titleStatus"], validators = [validators.optional()])
    vin = StringField("VIN", validators = [Length(max=40)])
    drive = SelectField("Drive", choices = dropdowns["drive"], validators = [validators.optional()])
    size = SelectField("Size", choices = dropdowns["size"], validators = [validators.optional()])
    vehicleType = SelectField("Vehicle Type", choices = dropdowns["vehicleType"], validators = [validators.optional()])
    paintColor = SelectField("Paint Color", choices = dropdowns["paintColor"], validators = [validators.optional()])
    priceStart = IntegerField("Minimum Price", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])
    priceEnd = IntegerField("Maximum Price", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])    
    yearStart = IntegerField("Minimum Year", validators=[validators.optional(), validators.NumberRange(min=1880, max=year + 1, message="Please enter a year between 1880 and {}".format(year + 1))])
    yearEnd = IntegerField("Maximum Year", validators=[validators.optional(), validators.NumberRange(min=1880, max=year + 1, message="Please enter a year between 1880 and {}".format(year + 1))])
    odometerStart = IntegerField("Minimum Odometer", validators=[validators.optional(), validators.NumberRange(min=0, max=10000000, message="Please enter a value between 0 and 10,000,000")])
    odometerEnd = IntegerField("Maximum Odometer", validators=[validators.optional(), validators.NumberRange(min=0, max=100000000, message="Please enter a value between 0 and 10,000,000")])
    

@app.route('/', methods=['GET', 'POST'])
def index():
    #render index.html with form passed through as a variable
    form = FilterForm()
    #validate_on_submit() runs when the form is submitted. we then redirect to search.html with the data fetched from queryForm.py
    if form.is_submitted():
        data = queryForm(form)
        return render_template("search.html", data = data)
    return render_template("index.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)