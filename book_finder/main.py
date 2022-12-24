from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .process import Scrape

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name = current_user.name)
    return render_template('index.html')


@main.route('/', methods=["POST"])
def index_input():
    userInput = request.form.get('userInput')
    return redirect(url_for('main.results', userInput = userInput))


@main.route('/<userInput>')
def results(userInput):
    obj = Scrape(userInput)
    obj.getSortedByPrice()
    sortByPrice = obj.products

    del obj
    if current_user.is_authenticated:
        return render_template('result_price.html', name = current_user.name, sortByPrice = sortByPrice)

    return render_template('result_price.html', sortByPrice = sortByPrice)

