# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import contextlib
import os
import tempfile

import dash_html_components as html


def _merge(a, b):  # pylint:disable=invalid-name
    return dict(a, **b)


def _omit(omitted_keys, d):  # pylint:disable=invalid-name
    return {k: v for k, v in d.items() if k not in omitted_keys}


def b64_to_str(content):
    """Bytes to pillow image"""
    data = content.encode('utf8').split(b';base64,')[1]
    decoded = base64.decodebytes(data)
    return decoded.decode('utf-8')


@contextlib.contextmanager
def temp(cleanup=True):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield tmp
    finally:
        tmp.close()  # closes the file, so we can right remove it
        cleanup and os.remove(tmp.name)


def save_file(filehandle, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode('utf8').split(b';base64,')[1]
    filehandle.write(base64.decodebytes(data))


def Card(children, **kwargs):  # pylint: disable=invalid-name
    return html.Section(
        children,
        style=_merge(
            {
                'padding': 10,
                'marginBottom': '1em',
                'marginTop': 0,
                'borderRadius': 5,
                'width': '100%',
                'border': 'thin lightgrey solid',
                # Remove possibility to select the text for better UX
                'userSelect': 'none',
                '-moz-user-select': 'none',
                '-webkit-user-select': 'none',
                '-msUserSelect': 'none',
            },
            kwargs.get('style', {}),
        ),
        **_omit(['style'], kwargs),
    )
