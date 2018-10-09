#this is where the magic happens, we currently have only one route but that will change

from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, IntegerField, SelectField, validators
from wtforms.validators import Length, ValidationError, DataRequired
from queryForm import queryForm
from queryDropdowns import queryDropdowns

app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)


class FilterForm(FlaskForm):
    #set up the form and grabbing dropdowns, a dictionary of unique values to populate select fields
    dropdowns = queryDropdowns()
    
    city = StringField("City", validators = [Length(max=40)])
    manufacturer = SelectField("Manufacturer", choices = dropdowns["manufacturer"], validators = [validators.optional()])    
    make = StringField("Make", validators = [Length(max=40)])
    condition = StringField("Condition", validators = [Length(max=40)])
    cylinders = SelectField("Cylinders", choices = dropdowns["cylinders"], validators = [validators.optional()])
    fuel = SelectField("Fuel", choices = dropdowns["fuel"], validators = [validators.optional()])
    transmission = SelectField("Transmission", choices = dropdowns["transmission"], validators = [validators.optional()])
    titleStatus = SelectField("Title Status", choices = dropdowns["titleStatus"], validators = [validators.optional()])
    vin = StringField("VIN", validators = [Length(max=40)])
    drive = SelectField("Drive", choices = dropdowns["drive"], validators = [validators.optional()])
    size = SelectField("Size", choices = dropdowns["size"], validators = [validators.optional()])
    vehicleType = SelectField("Vehicle Type", choices = dropdowns["vehicleType"], validators = [validators.optional()])
    paintColor = SelectField("Paint Color", choices = dropdowns["paintColor"], validators = [validators.optional()])
    price = IntegerField("Price", validators = [validators.optional()])
    year = IntegerField("Year", validators = [validators.optional()])
    odometer = IntegerField("Odometer", validators = [validators.optional()])

@app.route('/', methods=['GET', 'POST'])
def index():
    #render index.html with form passed through as a variable
    form = FilterForm()
    #validate_on_submit() runs when the form is submitted. we then redirect to search.html with the data fetched from queryForm.py
    if form.validate_on_submit():
        data = queryForm(form)
        return render_template("search.html", data = data)
    return render_template("index.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)