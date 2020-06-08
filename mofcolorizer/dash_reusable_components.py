# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import dash_html_components as html
from io import BytesIO as _BytesIO


def _merge(a, b):  # pylint:disable=invalid-name
    return dict(a, **b)


def _omit(omitted_keys, d):  # pylint:disable=invalid-name
    return {k: v for k, v in d.items() if k not in omitted_keys}


def b64_to_cif(string):
    """Bytes to pillow image"""
    decoded = base64.b64decode(string)
    buffer = _BytesIO(decoded)


def Card(children, **kwargs):  # pylint: disable=invalid-name
    return html.Section(
        children,
        style=_merge(
            {
                "padding": 20,
                "margin": 5,
                "borderRadius": 5,
                "border": "thin lightgrey solid",
                # Remove possibility to select the text for better UX
                "user-select": "none",
                "-moz-user-select": "none",
                "-webkit-user-select": "none",
                "-ms-user-select": "none",
            },
            kwargs.get("style", {}),
        ),
        **_omit(["style"], kwargs),
    )
