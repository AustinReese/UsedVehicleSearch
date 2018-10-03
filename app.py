from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, IntegerField, validators
from wtforms.validators import Length, ValidationError, DataRequired
from queryForm import queryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "CraigsistFilter"
bootstrap = Bootstrap(app)


class FilterForm(FlaskForm):
    city = StringField("City", validators = [Length(max=40)])
    manufacturer = StringField("Make", validators = [Length(max=40)])    
    make = StringField("Make", validators = [Length(max=40)])
    condition = StringField("Condition", validators = [Length(max=40)])
    cylinders = StringField("Cylinders", validators = [Length(max=40)])
    fuel = StringField("Fuel", validators = [Length(max=40)])
    transmission = StringField("Transmission", validators = [Length(max=40)])
    titleStatus = StringField("Title Status", validators = [Length(max=40)])
    vin = StringField("VIN", validators = [Length(max=40)])
    drive = StringField("Drive", validators = [Length(max=40)])
    size = StringField("Size", validators = [Length(max=40)])
    vehicleType = StringField("Type", validators = [Length(max=40)])
    paintColor = StringField("Paint Color", validators = [Length(max=40)])
    price = IntegerField("Price", validators = [validators.optional()])
    year = IntegerField("Make", validators = [validators.optional()])    
    odometer = IntegerField("Odometer", validators = [validators.optional()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    if form.validate_on_submit():
        data = query(form)
        return render_template("search.html", data = data)
    return render_template("index.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)