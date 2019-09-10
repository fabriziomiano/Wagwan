"""
The flask application package.
"""
import os
from flask import Flask
app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = os.urandom(24)
WWW_ROOT = "Wagwan"
PUBLIC_DIR = "static"
from Wagwan import api, views
