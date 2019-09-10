import os
import json
from flask import request, render_template, send_from_directory
from datetime import datetime
from Wagwan import app
from Wagwan.modules.wordcount import wordcount
from Wagwan.modules.ner import ner


@app.route('/api/run_wc', methods=['POST'])
def run_wc():
    """
    Run the word count analysis using the data
    passed in the form
    :return:
    """
    with open("settings.conf", "rb") as conf_in:
        conf = json.load(conf_in)
    form = request.form.to_dict()
    try:
        conf["access_token"] = form["access_token"]
        conf["page_id"] = form["page_id"]
        conf["post_id"] = form["post_id"]
        app.logger.info("Form submitted {}".format(form))
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
            barplot_path=barplot_filepath,
            wcloud_filepath=wcloud_filepath,
            csv_filepath=csv_filepath
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
    form = request.form.to_dict()
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
        app.logger.info("Form submitted {}".format(form))
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
            barplot_path=barplot_filepath,
            csv_filepath=csv_filepath
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


@app.route('/api/getcsv/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=app.root_path, filename=filename)
