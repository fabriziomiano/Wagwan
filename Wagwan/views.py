"""
Routes and views for the flask application.
"""
import json
from datetime import datetime
import os

from flask import render_template, request, send_from_directory

from Wagwan import app
from Wagwan.wordcount import wordcount
from Wagwan.ner import ner


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
        message="What's \"Wagwan\"?"
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


@app.route('/api/run_wc', methods=['POST'])
def run_wc():
    """
    Run the word count analysis using the data
    passed in the form
    :return:
    """
    with open("settings.conf", "rb") as conf_in:
        conf = json.load(conf_in)
    form = request.form
    try:
        conf["access_token"] = form["access_token"]
        conf["page_id"] = form["page_id"]
        conf["post_id"] = form["post_id"]
    except KeyError:
        error = "Please fill the form"
        return render_template(
            'wc.jade',
            title='Word Count',
            year=datetime.now().year,
            error=error
        )
    n_top_words = form["n_top_words"]
    if n_top_words != "":
        conf["n_top_words"] = n_top_words
    barplot_filepath, wcloud_filepath, csv_filepath = wordcount(conf)
    if barplot_filepath is not None and\
        wcloud_filepath is not None and\
            csv_filepath is not None:
        return render_template(
            'wc-results.jade',
            title='Wagwan',
            year=datetime.now().year,
            barplot_path=barplot_filepath.split("Wagwan")[1],
            wcloud_filepath=wcloud_filepath.split("Wagwan")[1],
            csv_filepath=csv_filepath.split("Wagwan")[1]
        )
    else:
        fb_url = "http://www.facebook.com/{}/posts/{}".format(conf["page_id"], conf["post_id"])
        error = (
            "Facebook did not return any comments!"
        )
        return render_template(
            'wc.jade',
            title='Word Count',
            year=datetime.now().year,
            fb_url=fb_url,
            error=error
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


@app.route('/api/run_ner', methods=['POST'])
def run_ner():
    """
    Run the named-entity recognizer using the data
    passed in the form
    :return:
    """
    supported_languages = ["it", "en"]
    with open("settings.conf", "rb") as conf_in:
        conf = json.load(conf_in)
    form = request.form
    try:
        conf["access_token"] = form["access_token"]
        conf["page_id"] = form["page_id"]
        conf["post_id"] = form["post_id"]
        conf["lang"] = form["lang"]
        if conf["lang"] not in supported_languages:
            error = "Please specify a supported language: en/it"
            return render_template(
                'ner.jade',
                title='Named-Entity Recognition',
                year=datetime.now().year,
                error=error
            )
    except KeyError:
        error = "Please fill the form"
        return render_template(
            'ner.jade',
            title='Named-Entity Recognition',
            year=datetime.now().year,
            error=error
        )
    n_top_entities = form["n_top_entities"]
    if n_top_entities != "":
        conf["n_top_entities"] = n_top_entities
    barplot_filepath, csv_filepath = ner(conf)
    if barplot_filepath is not None and \
            csv_filepath is not None:
        return render_template(
            'ner-results.jade',
            title='Named-Entity Recognition Results',
            year=datetime.now().year,
            barplot_path=barplot_filepath.split("Wagwan")[1],
            csv_filepath=csv_filepath.split("Wagwan")[1]
        )
    else:
        fb_url = "http://www.facebook.com/{}/posts/{}".format(conf["page_id"], conf["post_id"])
        error = "Facebook did not return any comments!"
        return render_template(
            'ner.jade',
            title='Named-Entity Recognition',
            year=datetime.now().year,
            fb_url=fb_url,
            error=error
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


@app.route('/api/getcsv/<path:filename>')
def serve_static(filename):
    app.logger.info("req {}".format(filename))
    root_dir = os.path.dirname(os.getcwd())
    app.logger.info("root dir {}".format(root_dir))
    return send_from_directory(os.path.join(root_dir, 'Wagwan/Wagwan'), filename)
