#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import hashlib

import flask
import json

from napkin.pages import utils as index_utils
from napkin.db import api as db_api


MSG_USER_REG = {
    '0': 'ok',
    '1': 'username already exists',
    '2': 'invalid password',
    '3': 'passwords are not same',
    '4': 'please enter the complete info',
    '5': 'please change the username',
}


def npk_users_password_sha(passwd):
    x = hashlib.sha512(passwd)
    s = x.hexdigest()
    return s


def npk_users_reg_valid(username, password, password2, *args, **kwargs):
    if not username or not password or not password2:
        return '4'

    if password != password2:
        return '3'

    try:
        u = db_api.user_filter(username=username)
        if u:
            return '1'
    except:
        return '5'

    return '0'


def npk_users_login_valid(username, password, *args, **kwargs):
    if not username or not password:
        return False

    try:
        u = db_api.user_filter(username=username)
        if not u:
            return False
        u = u[0]
        ps = u.passshadow
        px = npk_users_password_sha(password)
        if ps != px:
            return False
        else:
            return True
    except:
        return False


def app_load_web_users(app, opts=None):


    # Register Page
    @app.route('/u/reg/', methods=['POST', 'GET'])
    def user_reg():
        if flask.request.method == 'POST':
            username = flask.escape(flask.request.form.get('username'))
            password = flask.escape(flask.request.form.get('password'))
            password2 = flask.escape(flask.request.form.get('password2'))
            email = flask.escape(flask.request.form.get('email'))

            ret = npk_users_reg_valid(username, password, password2)

            if ret == '0':
                u = {}
                u['username'] = username
                u['email'] = email

                p = npk_users_password_sha(password)
                u['password'] = p[:32]
                u['passshadow'] = p

                u_o = db_api.user_create(u)

                flask.session['username'] = username
                return flask.redirect('/')
            else:
                msg = MSG_USER_REG.get(ret, 'something wrong')
                #flask.abort(400, msg)
                return flask.render_template('user/reg.html', msg=msg)
        else:
            if flask.session.get('username'):
                return flask.redirect('/')
            else:
                return flask.render_template('user/reg.html', msg='')

    # Login Page
    @app.route('/u/login/', methods=['POST', 'GET'])
    def user_login():
        if flask.request.method == 'POST':
            username = flask.escape(flask.request.form.get('username'))
            password = flask.escape(flask.request.form.get('password'))

            if npk_users_login_valid(username, password):
                flask.session['username'] = username
                #return flask.Response('ok')
                return flask.redirect('/')
            else:
                msg = 'Invalid username/password'
                #flask.abort(400, error)
                return flask.render_template('user/login.html', msg=msg)
        else:
            if flask.session.get('username'):
                return flask.redirect('/')
            else:
                return flask.render_template('user/login.html', msg='')

    @app.route('/u/logout/')
    def logout():
        flask.session.pop('username', None)
        return flask.redirect('/u/login')

    # return the application at the end
    return app
