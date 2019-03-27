# -*- coding: utf-8 -*-

import os
import tempfile

import pytest
from wublog import create_app, db
from sqlalchemy import text


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

q_insert_user = "INSERT INTO users_tbl (username, password_hash) VALUES ('test', 'pbkdf2:sha256:50000$qakQcWaJ$8ebd2584ddee684b0650b1433f5c3c7e85e4532d4b0d427227a7ca3cbdebd853'), ('u2', 'pbkdf2:sha256:50000$AIWZtm89$807b6f253e646eb032e8c24a1d2d7f374404f109d79cc0697777cc14eecacdd7');"
q_insert_post = "INSERT INTO posts_tbl (title, body, author_id, username, created) VALUES ('test title', 'test' || x'0a' || 'body', 1, 'test', '2018-01-01 00:00:00');"

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
    })

    # create the database and load test data
    with app.app_context():
        # init database
        db.init_app(app)
        db.create_all(app=app)
        # create test user and test post
        db.engine.execute(text(q_insert_user).execution_options(autocommit=True))
        db.engine.execute(text(q_insert_post).execution_options(autocommit=True))
        # db.session.commit()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
            # follow_redirects=True
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
