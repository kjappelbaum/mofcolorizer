# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from mofcolorizer import app, server

server = server
app = app

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True)
