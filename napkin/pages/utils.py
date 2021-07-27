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

import os
import codecs

import flask
import json

from napkin import config as sv_config


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


def login_required(f):
    def wrapper(*args, **kwargs):
        if flask.session.get('username') is None:
            return flask.redirect('/u/login')
        else:
            return f(*args, **kwargs)
    return wrapper


def flask_req_get_post_data(req):
    """
    data methods:
    ['add', 'clear', 'copy', 'fromkeys',
     'get', 'getlist', 'has_key',
     'items', 'iteritems', 'iterkeys',
     'iterlists', 'iterlistvalues', 'itervalues',
     'keys', 'lists', 'listvalues', 'pop', 'popitem',
     'popitemlist', 'poplist', 'setdefault', 'setlist',
     'setlistdefault', 'to_dict', 'update', 'values']
    """
    data_form = req.form
    if data_form:
        return data_form
    data_json = req.json
    if data_json:
        return data_json
    data_val = req.values
    if data_val:
        return data_val
    data_data = req.data
    return data_data


def flask_req_get_querystr(req):
    q_args = req.args
    if q_args:
        return q_args
    q_val = req.values
    if q_val:
        return q_val
    q_data = req.data
    return q_data


def flask_req_get_header_token(req):
    return req.headers.get('X-Auth-Token', None)


def flask_request_args_get_others(req, excluding=[]):
    args = flask_req_get_querystr(req)
    r = {}
    for k, v in args.items():
        if k and v and k not in excluding:
            r[k] = v
    return r


def file_read_local(file_name, *args, **kwargs):
    pth = os.path.join(BASE_DIR, file_name)
    ret = open(pth, 'rb').read()
    return ret


def file_read_local_md(file_name, *args, **kwargs):
    pth = os.path.join(BASE_DIR, file_name)
    infile = codecs.open(pth, mode="r", encoding="utf-8")
    text = infile.read()
    return text


def str_to_list_by(s, seq=[',']):
    for a in seq:
      s = s.replace(a, ' ')
    lst = s.split()
    return lst
