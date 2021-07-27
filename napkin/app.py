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

from napkin.pages import index as web_index
from napkin.pages import users as web_users
from napkin.pages import test as web_test
from napkin.pages import node as web_node
from napkin.pages import wiki as web_wiki


app = flask.Flask(__name__)

app.secret_key = ':P9}f)5;l:adB18&[_$+NaPkIn01]8'


# Index
app = web_index.app_load_web_index(app)

# Users
app = web_users.app_load_web_users(app)

# Test
app = web_test.app_load_web_test(app)

# Node
#app = web_node.app_load_web_node(app)

# Wiki
app = web_wiki.app_load_web_wiki(app)
