# -*- coding: utf-8 -*-
"""Used by gunicorn to spin off the app"""
from __future__ import absolute_import

from mofcolorizer import app, server  # pylint:disable=unused-import

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8091)
