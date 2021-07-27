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

import datetime

try:
    import pymongo
except:
    raise Exception('pymongo is not found!')

try:
    import mongoengine as me
except:
    raise Exception('mongoengine is not found!')


DB_MONGO_HOST = '192.168.146.54'
DB_MONGO_PORT = 27017
DB_MONGO_DATABASE = 'napkin'
DB_MONGO_USERNAME = ''
DB_MONGO_PASSWORD = ''


try:
    if DB_MONGO_USERNAME and DB_MONGO_PASSWORD:
        me.connect(DB_MONGO_DATABASE, host=DB_MONGO_HOST, port=DB_MONGO_PORT,
                   username=DB_MONGO_USERNAME, password=DB_MONGO_PASSWORD)
    else:
        me.connect(DB_MONGO_DATABASE, host=DB_MONGO_HOST, port=DB_MONGO_PORT)
except:
    raise Exception('can not connect to mongodb!')


class BASE(me.Document):
    pass


class TimeBase(me.Document):
    created_at = me.DateTimeField(default=datetime.datetime.now)
    updated_at = me.DateTimeField(default=datetime.datetime.now)
    deleted_at = me.DateTimeField()
    deleted = me.BooleanField(default=False)


class User(me.Document):
    username = me.StringField(max_length=50, required=True)
    email = me.StringField(required=True)
    first_name = me.StringField(max_length=50)
    last_name = me.StringField(max_length=50)
    password = me.StringField(max_length=64, required=True)
    passshadow = me.StringField(max_length=2048, required=True)
    info = me.DictField()  # metadata
    metadt = me.DictField()  # metadata
    #metadt = me.ListField(me.DictField())  # metadata


class WikiPage(me.Document):
    '''wiki pages'''
    __tablename__ = 'wiki_page'

    created_at = me.DateTimeField(default=datetime.datetime.now)
    updated_at = me.DateTimeField(default=datetime.datetime.now)
    deleted_at = me.DateTimeField()
    deleted = me.BooleanField(default=False)

    author = me.ReferenceField(User)
    author_name = me.StringField(max_length=255)

    title = me.StringField(max_length=255, required=True)
    content = me.StringField()
    html = me.StringField()
    #keywords = me.ListField(me.StringField(max_length=255))  # for search
    keywords = me.StringField(max_length=255)  # for search

    version = me.IntField(default=0, required=True)
    timestamp = me.StringField(max_length=255)

    state = me.StringField(max_length=255)  # ''/'open' 'lock'
    locked_at = me.DateTimeField()

    info = me.StringField(max_length=255)  #
    level = me.IntField(default=0)  # 0:normal 1:main

    #metadt = me.ListField(me.DictField())  # metadata
    metadt = me.DictField()  # metadata
