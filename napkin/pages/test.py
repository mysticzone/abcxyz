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

try:
    from napkin.db import db_sqlite
except:
    db_sqlite = None

try:
    from napkin.db import db_mongodb as db_mg
except:
    db_mg = None

from napkin.pages import utils as index_utils


def app_load_web_test(app, opts=None):
    app = app_load_web_test_test(app, opts)

    if db_sqlite:
        app = app_load_web_test_db_sqlite(app, opts)

    if db_mg:
        app = app_load_web_test_db_mongodb(app, opts)

    return app


def app_load_web_test_test(app, opts=None):

    # Test
    @app.route('/test', methods=['GET'])
    @app.route('/test/', methods=['GET'])
    def test():
        r = {}
        r['hello'] = 'world'
        return flask.Response(json.dumps(r), mimetype='application/json')

    # return the application at the end
    return app


def app_load_web_test_db_sqlite(app, opts=None):
    # Test db sqlite
    @app.route('/test/sqlt', methods=['GET'])
    def test_sqlt():
        conn = db_sqlite.sqlite_get_db()
        # Insert a row of data
        conn.execute("INSERT INTO stocks VALUES "
                     "('2006-01-05','BUY','RHAT',100,35.14)")
        conn.commit()

        r = db_sqlite.sqlite_query_db(conn, 'SELECT * FROM stocks')
        conn.close()

        return flask.Response(json.dumps(r), mimetype='application/json')

    # return the application at the end
    return app


def app_load_web_test_db_mongodb(app, opts=None):
    # Test db mongodb
    @app.route('/test/dbmg/useradd', methods=['GET'])
    def test_dbmg_useradd():
        ross = db_mg.User(email='ross@example.com')
        ross.first_name = 'Ross'
        ross.last_name = 'Lawley'
        ross.save()

        return flask.Response(ross.to_json(), mimetype='application/json')

    @app.route('/test/dbmg/userlist', methods=['GET'])
    def test_dbmg_userlist():
        #r = db_mg.User.objects.all()
        r = db_mg.User.objects(first_name='Ross')

        return flask.Response(r.to_json(), mimetype='application/json')

    # return the application at the end
    return app
