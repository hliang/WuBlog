import pytest
from flask import g, session
from wublog import db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    # test if new user exists in database
    with app.app_context():
        # init database
        db.init_app(app)
        db.create_all(app=app)
        assert db.engine.execute(
            "select * from users_tbl where username = 'a'"
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    # assert 0, response.data


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get('/auth/login').status_code == 200
    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


# def test_login2(auth):
#     # assert client.get('/auth/login').status_code == 200
#     response = auth.login(username="a", password="test")
#     assert b'Incorrect username' in response.data
#     response = auth.login(username="test", password="a")
#     assert b'Incorrect password' in response.data


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
    # ('test', 'test', b'test'),  # redirect to '/'
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username=username, password=password)
    assert message in response.data
    # assert 0, response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session