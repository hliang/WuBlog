# -*- coding: utf-8 -*-

import os


def test_database(app):
    """Ensure that the database exists."""
    db_exists = os.path.exists(app.config['DATABASE'])
    assert db_exists
    # assert 0, app.config['DATABASE']  # to show value
