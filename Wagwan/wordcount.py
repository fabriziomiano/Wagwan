import os
import time
from Wagwan import app
from Wagwan.classes.TextPreprocessor import TextPreprocessor
from Wagwan.classes.WordCloudPlotter import Plotter
from Wagwan.utils import (
    get_post_data, get_comments, do_wordcount,
    create_nonexistent_dir, save_barplot, data_to_tsv
)


def wordcount(conf):
    post_id = conf["post_id"]
    access_token = conf["access_token"]
    page_id = conf["page_id"]
    n_top_words = int(conf["n_top_words"])
    data_dir_path = conf["data_dir_name"]
    data_filename = "{}_{}{}".format(conf["data_wc_prefix"], post_id, ".csv")
    plots_dir_path = os.path.join(conf["plots_dir_name"], "single_posts", post_id)
    wc_plot_filename = "{}_{}{}".format(conf["wc_plot_filename"], post_id, ".png")
    wc_plot_filepath = os.path.join(plots_dir_path, wc_plot_filename)
    barplot_filename = "{}_{}{}".format(conf["barplot_filename"], post_id, ".png")
    barplot_filepath = os.path.join(plots_dir_path, barplot_filename)
    url_post = "https://www.facebook.com/{}/posts/{}".format(page_id, post_id)
    app.logger.info("Getting data for post {}".format(url_post))
    actual_post_id = page_id + "_" + post_id
    local_start = time.time()
    data = get_post_data(access_token, actual_post_id)
    comments = get_comments(data)
    if len(comments) == 0:
        app.logger.error(
            """Apparently, there are no comments at the selected post
            Check the actual post on its Facebook page 
            https://www.facebook.com/{}/posts/{}""".format(page_id, post_id)
        )
        return None, None, None
    elif len(comments) < 100:
        app.logger.warning(
            "Got {} comments. Not enough data "
            "to make much sense. Plots will be made regardless".format(len(comments))
        )
    else:
        app.logger.info("Got {} comments in {} seconds".format(
            len(comments), round((time.time() - local_start), 2)))
    local_start = time.time()
    preprocessed_comments = [TextPreprocessor(comm).preprocess() for comm in comments]
    app.logger.info("Preprocessed {} comments out of {} in {} seconds".format(
        len(preprocessed_comments), len(comments), round((time.time() - local_start), 1)))
    app.logger.info("Performing word count")
    wordcount_data = do_wordcount(preprocessed_comments)
    create_nonexistent_dir(data_dir_path)
    data_filepath = os.path.join(data_dir_path, data_filename)
    columns = ["word", "count"]
    data_to_tsv(wordcount_data, columns, data_filepath)
    app.logger.info("Saved {} words and their counts in {} ".format(
        len(wordcount_data), data_filepath))
    create_nonexistent_dir(plots_dir_path)
    plot_labels = ["Words", "Counts"]
    save_barplot(wordcount_data, plot_labels, n_top_words, barplot_filepath)
    app.logger.info("Bar plot saved at {}".format(barplot_filepath))
    unstemmed_comments = [TextPreprocessor(comm).base_preprocess() for comm in comments]
    long_string = " ".join(uc for uc in unstemmed_comments)
    p = Plotter(long_string)
    p.save_wordcloud_plot(wc_plot_filepath)
    app.logger.info("Word Cloud plot saved at {}".format(wc_plot_filepath))
    return barplot_filepath, wc_plot_filepath, data_filepath
