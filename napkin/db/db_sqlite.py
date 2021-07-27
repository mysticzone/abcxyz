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
import sqlite3


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_SQLITE_NAME = os.path.join(CURRENT_DIR, 'napkin.sqlite')
DB_SQLITE_SCHEMA = os.path.join(CURRENT_DIR, 'sqlite_schema.sql')


sqlite_db_g = None


def sqlite_connect_to_db():
    conn = sqlite3.connect(DB_SQLITE_NAME)
    return conn


def sqlite_get_db():
    return sqlite_connect_to_db()


def sqlite_close_db(conn):
    conn.close()


def sqlite_init_db():
    db = sqlite_get_db()
    with open(DB_SQLITE_SCHEMA, 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def sqlite_query_db(conn, query, args=(), one=False):
    """
    Here is how you can use it:

        for user in sqlite_query_db(conn, 'select * from users'):
            print user['username'], 'has the id', user['user_id']

    Or if you just want a single result:

        user = sqlite_query_db(conn, 'select * from users where username = ?',
                               [the_username], one=True)
        if user is None:
            print 'No such user'
        else:
            print the_username, 'has the id', user['user_id']
    """
    cur = conn.cursor().execute(query, args)
    rv = cur.fetchall()
    #conn.close()
    return (rv[0] if rv else None) if one else rv
