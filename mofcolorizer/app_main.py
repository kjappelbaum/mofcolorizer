# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pymatgen import Lattice, Structure

import crystal_toolkit.components as ctc

from . import dash_reusable_components as drc
from .app import app, server

structure = Structure(Lattice.cubic(4.2), ['Na', 'K'], [[0, 0, 0], [0.5, 0.5, 0.5]])

structure_component = ctc.StructureMoleculeComponent(
    structure,
    id='structure',
    bonding_strategy='JmolNN',
    color_scheme='Jmol',
)


def serve_layout():
    layout = html.Div(
        [
            html.Div([
                html.Div(
                    [
                        html.H1('MOFcolorizer', className='display-3', id='h1'),
                        html.P(
                            'This model attempts to predict the color of MOFs.',
                            className='lead',
                        ),
                        html.P(
                            'It is trained on subjective, categorical, assignments of colors to MOFs in the Cambridge Structural Database (CSD). We transformed the categorical labels into continuos ones using a survey.',
                            className='lead',
                        ),
                    ],
                    className='jumbotron',
                ),
                drc.Card([
                    dcc.Upload(
                        id='upload',
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
                ]),
                html.Div(
                    html.Div(
                        [
                            html.Div(
                                [
                                    structure_component.layout(size='400px'),
                                    structure_component.legend_layout(),
                                ],
                                className='col',
                            ),
                            html.Div([], className='col', id='resultdiv'),
                        ],
                        className='row',
                    ),
                    className='container',
                ),
            ]),
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
                        '© Laboratory of Molecular Simulation (LSMO), École polytechnique fédérale de Lausanne (EPFL)'),
                ],
                className='container',
            ),
        ],
        className='container',
        # tag for iframe resizer
        **{'data-iframe-height': ''})

    return layout


ctc.register_crystal_toolkit(app, layout=serve_layout())


@app.callback(
    Output('resultdiv', 'children'),
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')],
)
def main_callback(content, filename):
    print(filename)
    # check if new file was uploaded
    if new_filename and new_filename != filename:
        ...
