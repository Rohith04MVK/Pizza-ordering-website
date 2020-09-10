from flask import Flask, redirect, url_for, request, flash
from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError, InputRequired
import requests
toppings = ["Pepperoni", "Cheese", "Tomatoes",
            "Brocol", "Bacon", "Chilliflakes"]
toppings_price = {"Pepperoni": 28, "Cheese": 28,
                  "Tomatoes": 28, "Brocol": 28, "Bacon": 28, "Chilliflakes": 0}
price = {"Margherita": 280, "Pepperoni Feast": 290,
         "Veggie Supreme": 340, "Ultimate chicken": 305, "Original Pan": 210}
pizza = ["Margherita", "Pepperoni Feast",
         "Veggie Supreme", "Ultimate chicken", "Original Pan"]


def get_pincode():
    url = (f'https://api.postalpincode.in/pincode/{code}')
    response = requests.get(url, headers={"Accept": "application/json"})
    data = response.json()
    global Name
    Name = (data[0]['PostOffice'][0]['Name'])
    return Name


def pizza_validate(form, field):
    if field.data not in pizza:
        raise ValidationError('Enter the right name if the pizza')


app = Flask(__name__)
app.config['SECRET_KEY'] = '*9cnv8to4#64l5mvn8afb2owqldv4!26t4u'


class pincodeform(FlaskForm):
    pincode = IntegerField('Pincode:', validators=[InputRequired()])


class pizza_form(FlaskForm):
    pizza = StringField('Pizza:', validators=[InputRequired(), pizza_validate])


@app.route('/')
def index():
    return redirect(url_for('form'))

# GET and POST are the http verbs. Explore more
@app.route('/form', methods=["GET", "POST"])
def form():
    global code
    form = pincodeform() #Intialize or create object ?
    code = form.pincode.data

    if form.validate_on_submit():
        return redirect('/Welcome')
    return render_template('form.html', form=form)


@app.route('/Welcome', methods=['GET', "POST"])
def welcome():
    form = get_pincode()
    return render_template('welcome.html', form=form)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    form = pizza_form()
    pizzas = price
    global piz
    piz = form.pizza.data
    if form.validate_on_submit():
        return redirect(url_for('order'))
    return render_template('menu.html', form=form, pizzas=pizzas)


@app.route('/order', methods=['GET', 'POST'])
def order():
    global top # scope of this variable is global
    toppin = toppings_price
    top = (request.form.getlist('checkbox1'))
    if request.method == 'POST' and len(top) <= 4:
        return redirect(url_for('done'))
    return render_template('order.html', toppin=toppin)


@app.route('/done')
def done():
    form = bill()
    place = Name
    return render_template("done.html", form=form, place=place)


def bill():
    toppings_price_list = []
    for r in top:
        f = toppings_price.get(r)
        toppings_price_list.append(f)
    toppings_total = sum(toppings_price_list)
    bill = (int(price.get(piz))) + (toppings_total)
    return(str(bill) + " ₹")


if __name__ == '__main__':
    app.run(debug=True)
