from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def show():
    try:
        return render_template('main_page.html')
    except TemplateNotFound:
        abort(404)
