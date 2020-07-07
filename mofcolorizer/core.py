# -*- coding: utf-8 -*-
# pylint:disable=line-too-long
"""Calls the featurization function, loads the models and uses them to predict"""
from __future__ import absolute_import, print_function

import os

import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import joblib
from webcolors import rgb_to_hex

from .featurize import FeaturizationException, get_color_descriptors

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

SCALER = joblib.load(os.path.join(THIS_DIR, 'scaler_run_2020_06_08_12_59_1591613951.joblib'))
MODEL_MEDIAN = joblib.load(os.path.join(THIS_DIR, 'regressor_medianrun_2020_06_08_12_59_1591613951.joblib'))
MODEL_01 = joblib.load(os.path.join(THIS_DIR, 'regressor_0_1run_2020_06_08_12_59_1591613951.joblib'))
MODEL_09 = joblib.load(os.path.join(THIS_DIR, 'regressor_0_9run_2020_06_08_12_59_1591613951.joblib'))

CHEMICAL_FEATURES = [
    'mc_CRY-chi-0-all',
    'mc_CRY-chi-1-all',
    'mc_CRY-chi-2-all',
    'mc_CRY-chi-3-all',
    'mc_CRY-Z-0-all',
    'mc_CRY-Z-1-all',
    'mc_CRY-Z-2-all',
    'mc_CRY-Z-3-all',
    'mc_CRY-I-1-all',
    'mc_CRY-I-2-all',
    'mc_CRY-I-3-all',
    'mc_CRY-T-0-all',
    'mc_CRY-T-1-all',
    'mc_CRY-T-2-all',
    'mc_CRY-T-3-all',
    'mc_CRY-S-0-all',
    'mc_CRY-S-1-all',
    'mc_CRY-S-2-all',
    'mc_CRY-S-3-all',
    'D_mc_CRY-chi-1-all',
    'D_mc_CRY-chi-2-all',
    'D_mc_CRY-chi-3-all',
    'D_mc_CRY-Z-1-all',
    'D_mc_CRY-Z-2-all',
    'D_mc_CRY-Z-3-all',
    'D_mc_CRY-T-1-all',
    'D_mc_CRY-T-2-all',
    'D_mc_CRY-T-3-all',
    'D_mc_CRY-S-1-all',
    'D_mc_CRY-S-2-all',
    'D_mc_CRY-S-3-all',
    'func-chi-0-all',
    'func-chi-1-all',
    'func-chi-2-all',
    'func-chi-3-all',
    'func-Z-0-all',
    'func-Z-1-all',
    'func-Z-2-all',
    'func-Z-3-all',
    'func-I-1-all',
    'func-I-2-all',
    'func-I-3-all',
    'func-T-0-all',
    'func-T-1-all',
    'func-T-2-all',
    'func-T-3-all',
    'func-S-0-all',
    'func-S-1-all',
    'func-S-2-all',
    'func-S-3-all',
    'func-alpha-0-all',
    'func-alpha-1-all',
    'func-alpha-2-all',
    'func-alpha-3-all',
    'D_func-chi-1-all',
    'D_func-chi-2-all',
    'D_func-chi-3-all',
    'D_func-Z-1-all',
    'D_func-Z-2-all',
    'D_func-Z-3-all',
    'D_func-T-1-all',
    'D_func-T-2-all',
    'D_func-T-3-all',
    'D_func-S-2-all',
    'D_func-S-3-all',
    'D_func-alpha-1-all',
    'D_func-alpha-2-all',
    'D_func-alpha-3-all',
    'f-lig-chi-0',
    'f-lig-chi-1',
    'f-lig-chi-2',
    'f-lig-chi-3',
    'f-lig-Z-0',
    'f-lig-Z-1',
    'f-lig-Z-2',
    'f-lig-Z-3',
    'f-lig-I-0',
    'f-lig-I-1',
    'f-lig-I-2',
    'f-lig-I-3',
    'f-lig-T-0',
    'f-lig-T-1',
    'f-lig-T-2',
    'f-lig-T-3',
    'f-lig-S-0',
    'f-lig-S-1',
    'f-lig-S-2',
    'f-lig-S-3',
    'lc-chi-0-all',
    'lc-chi-1-all',
    'lc-chi-2-all',
    'lc-chi-3-all',
    'lc-Z-0-all',
    'lc-Z-1-all',
    'lc-Z-2-all',
    'lc-Z-3-all',
    'lc-I-2-all',
    'lc-I-3-all',
    'lc-T-0-all',
    'lc-T-1-all',
    'lc-T-2-all',
    'lc-T-3-all',
    'lc-S-3-all',
    'lc-alpha-0-all',
    'lc-alpha-1-all',
    'lc-alpha-2-all',
    'lc-alpha-3-all',
    'D_lc-chi-2-all',
    'D_lc-chi-3-all',
    'D_lc-Z-1-all',
    'D_lc-Z-2-all',
    'D_lc-Z-3-all',
    'D_lc-T-1-all',
    'D_lc-T-2-all',
    'D_lc-T-3-all',
    'D_lc-alpha-1-all',
    'D_lc-alpha-2-all',
    'D_lc-alpha-3-all',
    'tertiary_amide_sum',
    'ester_sum',
    'carbonyl_sum',
    'logP_sum',
    'MR_sum',
    'aromatic_rings_sum',
    'dbonds_sum',
    'abonds_sum',
    'tertiary_amide_mean',
    'ester_mean',
    'carbonyl_mean',
    'logP_mean',
    'MR_mean',
    'aromatic_rings_mean',
    'dbonds_mean',
    'abonds_mean',
    'sum-func-chi-0-all',
    'sum-func-chi-1-all',
    'sum-func-chi-2-all',
    'sum-func-chi-3-all',
    'sum-func-Z-0-all',
    'sum-func-Z-1-all',
    'sum-func-Z-2-all',
    'sum-func-Z-3-all',
    'sum-func-I-0-all',
    'sum-func-I-1-all',
    'sum-func-I-2-all',
    'sum-func-I-3-all',
    'sum-func-T-0-all',
    'sum-func-T-1-all',
    'sum-func-T-2-all',
    'sum-func-T-3-all',
    'sum-func-S-0-all',
    'sum-func-S-1-all',
    'sum-func-S-2-all',
    'sum-func-S-3-all',
    'sum-func-alpha-0-all',
    'sum-func-alpha-1-all',
    'sum-func-alpha-2-all',
    'sum-func-alpha-3-all',
    'sum-D_func-chi-1-all',
    'sum-D_func-chi-2-all',
    'sum-D_func-chi-3-all',
    'sum-D_func-Z-1-all',
    'sum-D_func-Z-2-all',
    'sum-D_func-Z-3-all',
    'sum-D_func-T-1-all',
    'sum-D_func-T-2-all',
    'sum-D_func-T-3-all',
    'sum-D_func-S-1-all',
    'sum-D_func-S-2-all',
    'sum-D_func-S-3-all',
    'sum-D_func-alpha-1-all',
    'sum-D_func-alpha-2-all',
    'sum-D_func-alpha-3-all',
    'sum-f-lig-chi-0',
    'sum-f-lig-chi-1',
    'sum-f-lig-chi-2',
    'sum-f-lig-chi-3',
    'sum-f-lig-Z-0',
    'sum-f-lig-Z-1',
    'sum-f-lig-Z-2',
    'sum-f-lig-Z-3',
    'sum-f-lig-I-0',
    'sum-f-lig-I-1',
    'sum-f-lig-I-2',
    'sum-f-lig-I-3',
    'sum-f-lig-T-0',
    'sum-f-lig-T-1',
    'sum-f-lig-T-2',
    'sum-f-lig-T-3',
    'sum-f-lig-S-0',
    'sum-f-lig-S-1',
    'sum-f-lig-S-2',
    'sum-f-lig-S-3',
    'sum-lc-chi-0-all',
    'sum-lc-chi-1-all',
    'sum-lc-chi-2-all',
    'sum-lc-chi-3-all',
    'sum-lc-Z-0-all',
    'sum-lc-Z-1-all',
    'sum-lc-Z-2-all',
    'sum-lc-Z-3-all',
    'sum-lc-I-0-all',
    'sum-lc-I-1-all',
    'sum-lc-I-2-all',
    'sum-lc-I-3-all',
    'sum-lc-T-0-all',
    'sum-lc-T-1-all',
    'sum-lc-T-2-all',
    'sum-lc-T-3-all',
    'sum-lc-S-0-all',
    'sum-lc-S-1-all',
    'sum-lc-S-2-all',
    'sum-lc-S-3-all',
    'sum-lc-alpha-0-all',
    'sum-lc-alpha-1-all',
    'sum-lc-alpha-2-all',
    'sum-lc-alpha-3-all',
    'sum-D_lc-chi-1-all',
    'sum-D_lc-chi-2-all',
    'sum-D_lc-chi-3-all',
    'sum-D_lc-Z-1-all',
    'sum-D_lc-Z-2-all',
    'sum-D_lc-Z-3-all',
    'sum-D_lc-T-1-all',
    'sum-D_lc-T-2-all',
    'sum-D_lc-T-3-all',
    'sum-D_lc-S-1-all',
    'sum-D_lc-S-2-all',
    'sum-D_lc-S-3-all',
    'sum-D_lc-alpha-1-all',
    'sum-D_lc-alpha-2-all',
    'sum-D_lc-alpha-3-all',
    'sum-mc_CRY-chi-0-all',
    'sum-mc_CRY-chi-1-all',
    'sum-mc_CRY-chi-2-all',
    'sum-mc_CRY-chi-3-all',
    'sum-mc_CRY-Z-0-all',
    'sum-mc_CRY-Z-1-all',
    'sum-mc_CRY-Z-2-all',
    'sum-mc_CRY-Z-3-all',
    'sum-mc_CRY-I-0-all',
    'sum-mc_CRY-I-1-all',
    'sum-mc_CRY-I-2-all',
    'sum-mc_CRY-I-3-all',
    'sum-mc_CRY-T-0-all',
    'sum-mc_CRY-T-1-all',
    'sum-mc_CRY-T-2-all',
    'sum-mc_CRY-T-3-all',
    'sum-mc_CRY-S-0-all',
    'sum-mc_CRY-S-1-all',
    'sum-mc_CRY-S-2-all',
    'sum-mc_CRY-S-3-all',
    'sum-D_mc_CRY-chi-1-all',
    'sum-D_mc_CRY-chi-2-all',
    'sum-D_mc_CRY-chi-3-all',
    'sum-D_mc_CRY-Z-1-all',
    'sum-D_mc_CRY-Z-2-all',
    'sum-D_mc_CRY-Z-3-all',
    'sum-D_mc_CRY-T-1-all',
    'sum-D_mc_CRY-T-2-all',
    'sum-D_mc_CRY-T-3-all',
    'sum-D_mc_CRY-S-1-all',
    'sum-D_mc_CRY-S-2-all',
    'sum-D_mc_CRY-S-3-all',
]


def _featurize(cif):
    """Runs featurization and returns none in case of FeaturizationException"""
    try:
        descriptors = get_color_descriptors(cif)
        return descriptors[CHEMICAL_FEATURES]
    except FeaturizationException as e:
        print(e)
        return None


def predict(cif):
    """Outputs a table with predictions and a div with explanaition if the prediction worked"""

    features = _featurize(cif)

    if not isinstance(features, pd.DataFrame):  # pylint:disable=no-else-return
        # Featurization exception occured, we do not return a results table but rather an error message
        return dbc.Alert(
            'An error occured during the featurization. Ensure that your structure is valid, non-disordered and contains no clashing atoms.',
            dismissable=True,
            color='warning',
            style={
                'margin-left': '3rem',
                'margin-right': '1rem'
            })
    else:
        features = SCALER.transform(features)
        prediction_01 = MODEL_01.predict(features) * 255
        prediction_09 = MODEL_09.predict(features) * 255
        prediction_median = MODEL_MEDIAN.predict(features) * 255

        prediction_median_rounded = [int(c) for c in prediction_median[0]]
        prediction_01_rounded = [int(c) for c in prediction_01[0]]
        prediction_09_rounded = [int(c) for c in prediction_09[0]]
        hex_median = [rgb_to_hex((int(c[0]), int(c[1]), int(c[2]))) for c in prediction_median][0]
        hex_01 = [rgb_to_hex((int(c[0]), int(c[1]), int(c[2]))) for c in prediction_01][0]
        hex_09 = [rgb_to_hex((int(c[0]), int(c[1]), int(c[2]))) for c in prediction_09][0]
        return html.Div([
            dbc.Table([
                html.Thead([html.Td(), html.Td('Median'),
                            html.Td('10 %'), html.Td('90 %')]),
                html.Tr([
                    html.Td('color'),
                    html.Td(style={'background-color': hex_median}),
                    html.Td(style={'background-color': hex_01}),
                    html.Td(style={'background-color': hex_09}),
                ]),
                html.Tr([
                    html.Td('RGB'),
                    html.Td('{} {} {}'.format(prediction_median_rounded[0], prediction_median_rounded[1],
                                              prediction_median_rounded[2])),
                    html.Td('{} {} {}'.format(prediction_01_rounded[0], prediction_01_rounded[1],
                                              prediction_01_rounded[2])),
                    html.Td('{} {} {}'.format(prediction_09_rounded[0], prediction_09_rounded[1],
                                              prediction_09_rounded[2])),
                ]),
                html.Tr([
                    html.Td('Hex'),
                    html.Td(hex_median),
                    html.Td(hex_01),
                    html.Td(hex_09),
                ]),
            ],
                      bordered=True,
                      style={
                          'width': '90%',
                          'margin-left': '5%'
                      }),
            html.P([
                'We show three different colors as the predictions a model makes are samples from some distribution.'
                ' The most important point is the median, which is the center of the distribution and this should be closest to the real color.',
                ' The 10% and 20% quantiles represent the lower and upper errorbars.',
                ' If the model is quite sure about the prediction, the colors will be close to the median.'
            ],
                   style={
                       'width': '90%',
                       'margin-left': '5%'
                   })
        ])
