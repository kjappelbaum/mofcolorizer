# -*- coding: utf-8 -*-
# pylint:disable=line-too-long
"""Core of the flask app"""
from __future__ import absolute_import, print_function

import logging

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from pymatgen import Lattice, Structure

import crystal_toolkit.components as ctc
import dash_bootstrap_components as dbc
from flask_session import Session

from . import dash_reusable_components as drc
from .core import predict

__version__ = 'v0.1-alpha (20/07/2020)'

EXTERNAL_STYLESHEETS = ['./assets/style.css', './assets/vis.min.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(  # pylint:disable=invalid-name
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    meta_tags=[
        {
            'charset': 'utf-8'
        },
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        # needed for iframe resizer
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        },
    ],
)

server = app.server  # pylint:disable=invalid-name
app.title = 'mofcolorizer'

STRUCTURE = Structure(Lattice.cubic(4.2), ['Na', 'K'], [[0, 0, 0], [0.5, 0.5, 0.5]])

structure_component = ctc.StructureMoleculeComponent(  # pylint:disable=invalid-name
    STRUCTURE,
    id='structure',
    bonding_strategy='JmolNN',
    color_scheme='Jmol',
)

layout = html.Div(  # pylint:disable=invalid-name
    [
        dcc.Store(id='memorystore'),
        html.Div(
            [
                html.Div([
                    html.H1(['MOF', html.I('colorizer')], className='display-3', id='h1'),
                    html.P(
                        'This model attempts to predict the color of MOFs.',
                        className='lead',
                    ),
                    html.P(
                        [
                            'It is trained on subjective, categorical, assignments of colors to MOFs in the Cambridge Structural Database (CSD).',
                            ' We transformed the categorical labels into continuos ones using a survey.'
                        ],
                        className='lead',
                    ),
                ],
                         className='jumbotron',
                         style={
                             'margin-bottom': '1rem',
                             'padding-bottom': '2rem'
                         }),
                drc.Card([
                    dcc.Upload(
                        id='upload_cif',
                        children=[
                            'Drag and Drop or ',
                            html.A('Select a cif'),
                        ],
                        style={
                            'width': '100%',
                            'height': '50px',
                            'lineHeight': '50px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                        },
                        accept='.cif',
                    ),
                    html.Div('', id='upload_info'),
                ],),
                html.Div(
                    html.Div(
                        [
                            html.Div([
                                structure_component.layout(),
                                structure_component.legend_layout(),
                            ],
                                     className='col-md-4',
                                     style={'width': '100%'}),
                            html.Div(dcc.Loading([html.Div(id='resultdiv')]), className='col-md-8'),
                        ],
                        className='row',
                    ),
                    className='container',
                ),
            ],
            className='container',
        ),
        html.Div(
            [
                html.Div([
                    html.H2('About', className='display-4'),
                    html.P('For more details, please have a look at our paper.'),
                    html.P([
                        'If you want to learn more, feel free to contact ',
                        html.A('Kevin', href='mailto:kevin.jablonka@epfl.ch'),
                        '.',
                    ]),
                    html.H2('Technical Details', className='display-4'),
                    html.P([
                        'This app was implemented using ',
                        html.A(
                            'crystal toolkit',
                            href='https://docs.crystaltoolkit.org/index.html',
                        ),
                        ' and ',
                        html.A('Dash', href='https://plot.ly/dash/'),
                        '.',
                        ' This app can appear slow due to I/O operations that were not optimized for use on the web.',
                    ]),
                    html.H2('Privacy', className='display-4'),
                    html.P('We will store no personal data that can identify you.'),
                ],),
                html.Hr(),
                html.Footer(
                    '© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL). Web app version {}.'
                    .format(__version__)),
            ],
            className='container',
        ),
    ],
    className='container',
    # tag for iframe resizer
    **{'data-iframe-height': ''})

ctc.register_crystal_toolkit(app, layout=layout)


@app.callback(
    Output('resultdiv', 'children'),
    [Input('memorystore', 'modified_timestamp')],
    [State('memorystore', 'data')],
)
def run_prediction(_, store):
    """Returns the prediction table"""
    app.logger.info('triggering prediction update')
    try:
        if store['structure'] is not None:
            with drc.temp() as tempfilehandle:
                s = Structure.from_dict(store['structure'])  # pylint: disable=invalid-name
                s.to(filename=tempfilehandle.name, fmt='cif')
                prediction = predict(tempfilehandle.name)
            return prediction

        raise PreventUpdate
    except Exception as e:  # pylint:disable=broad-except,invalid-name
        print(e)
        raise PreventUpdate


@app.callback(
    [Output('memorystore', 'data'), Output('upload_info', 'children')],
    [Input('upload_cif', 'contents')],
    [State('upload_cif', 'filename'), State('memorystore', 'data')],
)
def update_structure(content, new_filename, store):
    """Loads the structure into the memory div"""
    app.logger.info('triggered structure update callback')
    try:
        filename = store['filename']

        # check if new file was uploaded
        if new_filename and new_filename != filename:
            app.logger.info('updating structure')
            structure_str = drc.b64_to_str(content)
            # print(structure_str)
            try:
                structure_object = Structure.from_str(structure_str, fmt='cif')
                str_dict = structure_object.as_dict()
                store['filename'] = new_filename
                # session["structure"] = str_dict
                # session["filename"] = new_filename
                # We need to give the user somehow feedback ...git
                store['structure'] = str_dict
                return store, ''
            except Exception:  # pylint:disable=broad-except
                return store, 'There has been a problem with loading the structure.'

    except Exception:  # pylint:disable=broad-except
        store = {'filename': None, 'structure': None}

    return store, ''


@app.callback(
    Output(structure_component.id(), 'data'),
    [Input('memorystore', 'modified_timestamp')],
    [State('memorystore', 'data')],
)
def update_structure_viz(_, store):
    """Updates the crystaltoolkit visualizer"""
    app.logger.info('triggering structure viz update')
    try:
        if store['structure'] is not None:
            return Structure.from_dict(store['structure'])
        raise PreventUpdate
    except Exception:  # pylint:disable=broad-except
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
