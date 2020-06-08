# -*- coding: utf-8 -*-
from __future__ import absolute_import

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import joblib
import pandas as pd

from colorml.featurize import FeaturizationException, get_color_descriptors

# SCALER = joblib.load()
# MODEL_MEDIAN = joblib.load()
# MODEL_01 = joblib.load()
# MODEL_09 = joblib.load()


def _featurize(cif):
    try:
        descriptors = get_color_descriptors(cif)
        return descriptors
    except FeaturizationException:
        return None


def predict(cif):
    features = _featurize(cif)

    if features is None:
        # Featurization exception occured, we do not return a results table but rather an error message
        return html.Div(
            'An error occured during the featurization. Ensure that your strucutre is valid, non-disordered and contains no clashing atoms.'
        )
    else:
        return dbc.Table(
            [
                html.Thead([html.Td('Median'), html.Td('10 %'), html.Td('90 %')]),
                html.Tr([
                    html.Td(''),
                    html.Td(''),
                    html.Td(''),
                ]),
                html.Tr([
                    html.Td(''),
                    html.Td(''),
                    html.Td(''),
                ]),
            ],
            bordered=True,
        )
