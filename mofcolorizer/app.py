# -*- coding: utf-8 -*-
"""Setting up the app"""
from __future__ import absolute_import

import dash
from flask_session import Session

EXTERNAL_STYLESHEETS = [
    "./assets/style.css",
    "./assets/vis.min.css",
]

sess = Session()  # pylint:disable=invalid-name

app = dash.Dash(  # pylint:disable=invalid-name
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    meta_tags=[
        {"charset": "utf-8"},
        {"http-equiv": "X-UA-Compatible", "content": "IE=edge"},
        # needed for iframe resizer
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

server = app.server  # pylint:disable=invalid-name

app.config.suppress_callback_exceptions = True
app.title = "mofcolorizer"

server.config.from_object("config.Config")
