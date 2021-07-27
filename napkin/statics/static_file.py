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
import os


def app_load_static_file(app, opts=None):

    # NOTE(likun): change the static_folder of app directly
    # in order to send static file
    #app._static_folder = '../' + app._static_folder

    @app.route('/static/js/<path:path>')
    def static_proxy_js(path):
        # send_static_file will guess the correct MIME type
        #return app.send_static_file(os.path.join('js', path))
        return flask.send_from_directory(
            os.path.join(app._static_folder, 'js'), path)

    @app.route('/static/css/<path:path>')
    def static_proxy_css(path):
        return flask.send_from_directory(
            os.path.join(app._static_folder, 'css'), path)

    @app.route('/static/fonts/<path:path>')
    def static_proxy_fonts(path):
        return flask.send_from_directory(
            os.path.join(app._static_folder, 'fonts'), path)

    @app.route('/static/img/<path:path>')
    def static_proxy_img(path):
        return flask.send_from_directory(
            os.path.join(app._static_folder, 'img'), path)

    @app.route('/static/plugins/<path:path>')
    def static_proxy_plugins(path):
        return flask.send_from_directory(
            os.path.join(app._static_folder, 'plugins'), path)

    return app