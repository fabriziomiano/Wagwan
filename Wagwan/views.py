"""
Routes and views for the flask application.
"""
import json
from datetime import datetime
import os

from flask import render_template, request, send_file, send_from_directory

from Wagwan import app
from Wagwan.wordcount import wordcount


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.jade',
        title='Wagwan',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/wc')
def wc():
    """Renders the wc page."""
    return render_template(
        'wc.jade',
        title='Word Count',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/api/runwc', methods=['POST'])
def runwc():
    """
    Run the word count analysis using the data
    passed in the form
    :return:
    """
    with open("settings.conf", "rb") as conf_in:
        conf = json.load(conf_in)
    form = request.form
    conf["access_token"] = form.get("access_token")
    conf["page_id"] = form.get("page_id")
    conf["post_id"] = form.get("post_id")
    if form["n_top_words"] != "":
        conf["n_top_words"] = form.get("n_top_words")
    if form["n_top_entities"] != "":
        conf["n_top_entities"] = form.get("n_top_entities")
    # TODO check variables and return status code 400 if some of them aren't specified
    barplot_filepath, wcloud_filepath, csv_filepath = wordcount(conf)
    return render_template(
        'wc-results.jade',
        title='Wagwan',
        year=datetime.now().year,
        barplot_path=barplot_filepath.split("Wagwan")[1],
        wcloud_filepath=wcloud_filepath.split("Wagwan")[1],
        csv_filepath=csv_filepath.split("Wagwan")[1]
    )


@app.route('/wc-results')
def wc_results():
    """
    Render wc-results page. More for dev purposes
    """
    return render_template(
        'wc-results.jade',
        title='Wagwan',
        year=datetime.now().year
    )


@app.route('/api/getcsv/<path:filename>')
def serve_static(filename):
    app.logger.info("req {}".format(filename))
    root_dir = os.path.dirname(os.getcwd())
    app.logger.info("root dir {}".format(root_dir))
    return send_from_directory(os.path.join(root_dir, 'Wagwan/Wagwan'), filename)
