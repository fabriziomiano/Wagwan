"""
Routes and views for the flask application.
"""
from datetime import datetime
import os

from flask import render_template, send_from_directory

from Wagwan import app


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.jade'), 404


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.jade',
        title='Home',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.now().year,
        message='Hit me up!'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.now().year,
        message="Why \"Wagwan\"?"
    )


@app.route('/wc')
def wc():
    """Renders the wc page."""
    return render_template(
        'wc.jade',
        title='Smart Word Count',
        year=datetime.now().year
    )


@app.route('/ner')
def render_ner():
    """Renders the ner page."""
    return render_template(
        'ner.jade',
        title='Named-Entity Recognition',
        year=datetime.now().year
    )


@app.route('/wc-results')
def wc_results():
    """
    Render wc-results page
    """
    return render_template(
        'wc-results.jade',
        title='Word Count Results',
        year=datetime.now().year
    )


@app.route('/ner-results')
def ner_results():
    """
    Render ner-results page
    """
    return render_template(
        'ner-results.jade',
        title='NER Results',
        year=datetime.now().year
    )
