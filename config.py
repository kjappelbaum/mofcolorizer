# -*- coding: utf-8 -*-
"""App configuration."""
from __future__ import absolute_import

import os
from os import environ


class Config:  # pylint:disable=too-few-public-methods
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', 'B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-Session
    SESSION_TYPE = 'filesystem'  # there is some issue with images getting to large for the heroku redis
