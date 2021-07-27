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
"""
Physical Node Info
"""

import flask
import json

from napkin.pages import utils as index_utils
from napkin.db import api as db_api


URL_PREFIX_NODE_WEB = '/node'


def app_load_web_node(app, opts=None):

    # Node List Page
    @app.route(URL_PREFIX_NODE_WEB + '/list/')
    ##@index_utils.login_required
    def node_list():
        nodes = db_api.node_get_all()
        ns = []
        for node in nodes:
            info = db_api.node_info_get(node.info.id)
            node.infos = info
            ns.append(node)
        #return flask.Response(nodes.to_json(),
        #                      mimetype='application/json')
        return flask.render_template('node/list.html', nodes=ns)

    # Node Stats Page
    @app.route(URL_PREFIX_NODE_WEB + '/stats/')
    ##@index_utils.login_required
    def node_stats():
        args = index_utils.flask_req_get_querystr(flask.request)
        if args:
            prefix = args.get('prefix', '')
            name = args.get('name', '')
            metric = args.get('metric', 'cpu')
            cnt = args.get('cnt', 20)
            page = args.get('page', 0)
        else:
            prefix = ''
            name = ''
            metric = 'cpu'
            cnt = 20
            page = 0

        return flask.render_template('node/stats.html',
                                     prefix=prefix, name=name,
                                     metric=metric,
                                     cnt=str(cnt), page=str(page))

    # return the application at the end
    return app
