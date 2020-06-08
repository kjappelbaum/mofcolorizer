# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from . import app_main
from .app import app, server
from .app_main import serve_layout

app.layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='page-content')])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
)
def display_page(pathname):
    """Display the layout as function of the url"""

    app.logger.info('Pathname is {}'.format(pathname))
    if pathname == '/':
        return serve_layout()

    return serve_layout()


if __name__ == '__main__':
    app.run_server(debug=True)
