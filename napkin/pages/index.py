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

import flask
import json

from napkin.pages import utils as index_utils


def app_load_web_index(app, opts=None):

    # Index Page
    @app.route('/')
    @index_utils.login_required
    def index():
        theme = 'default'
        username = flask.session.get('username')
        if username:
            username = flask.escape(username)
        return flask.render_template('index.html', theme=theme,
                                     username=username)

    return app
