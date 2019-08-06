import os
from datetime import datetime
from flask import render_template
import spacy
from Wagwan import app
from Wagwan.utils import (
    get_post_data, get_comments, save_barplot,
    create_nonexistent_dir, data_to_tsv, get_entities, count_entities
)


def ner(conf):
    supported_languages = ["it", "en"]
    lang = conf["lang"]
    if lang not in supported_languages:
        error = "Please provide a valid language. Supported: 'en', 'it'"
        app.logger.error(error)
        return render_template(
            'ner-results.jade',
            year=datetime.now().year,
            error=error
        )
    else:
        try:
            model = conf.get(lang)
            nlp = spacy.load(model)
        except OSError:
            error = "Could not find model in conf file. Please double check"
            app.logger.error(error)
            return render_template(
                'ner.jade',
                year=datetime.now().year,
                error=error
            )
    access_token = conf["access_token"]
    page_id = conf["page_id"]
    post_id = conf["post_id"]
    n_top_entities = conf["n_top_entities"]
    data_dir_path = conf["data_dir_name"]
    data_filename = "{}_{}{}".format(conf["data_entities_prefix"], post_id, ".csv")
    plots_dir_path = conf["plots_dir_name"]
    barplot_filename = "{}_{}{}".format(conf["barplot_filename"], post_id, "_ner.png")
    barplot_filepath = os.path.join(plots_dir_path, barplot_filename)
    actual_post_id = page_id + "_" + post_id
    url_post = "https://www.facebook.com/posts/{}".format(actual_post_id)
    app.logger.info("Getting data for post {}".format(url_post))
    data = get_post_data(access_token, actual_post_id)
    comments = get_comments(data)
    if len(comments) == 0:
        app.logger.error(
            """Apparently, there are no comments at the selected post
            Check the actual post on its Facebook page 
            https://www.facebook.com/{}/posts/{}""".format(page_id, post_id)
        )
        return None, None
    elif len(comments) < 100:
        app.logger.warning(
            "Got {} comments. Not enough data "
            "to make much sense. Plots will be made regardless".format(len(comments))
        )
    else:
        app.logger.info("Got {} comments".format(len(comments)))
    entities = []
    for comment in comments:
        ents = get_entities(nlp, comment)
        entities.extend(ents)
    app.logger.info(
        "Extracted {} entities out of {} comments".format(
            len(entities), len(comments))
    )
    entities_data = count_entities(entities)
    create_nonexistent_dir(data_dir_path)
    data_filepath = os.path.join(data_dir_path, data_filename)
    columns = ["entities", "count"]
    data_to_tsv(entities_data, columns, data_filepath)
    app.logger.info("Saved {} unique entities and their counts in {} ".format(
        len(entities_data), data_filepath))
    create_nonexistent_dir(plots_dir_path)
    plot_labels = ["Entities", "Counts"]
    save_barplot(entities_data, plot_labels, n_top_entities, barplot_filepath)
    app.logger.info("Bar plot saved at {}".format(barplot_filepath))
    return barplot_filepath, data_filepath
