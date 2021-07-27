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
MongoDB API with MongoEngine

docs:
  1. http://docs.mongoengine.org/
  2. http://docs.mongoengine.org/guide/querying.html
"""

from napkin.db import db_mongodb as db_mg


'''
dir(o):
['DoesNotExist', 'MultipleObjectsReturned',
 '_BaseDocument__expand_dynamic_values',
 '_BaseDocument__get_field_display', '_BaseDocument__set_field_display',
 '__class__', '__contains__', '__delattr__', '__dict__', '__doc__', '__eq__',
 '__format__', '__getattribute__', '__getitem__', '__getstate__', '__hash__',
 '__init__', '__iter__', '__len__', '__metaclass__', '__module__', '__ne__',
 '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
 '__setitem__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__',
 '__weakref__', '_auto_id_field', '_build_index_spec', '_build_index_specs',
 '_changed_fields', '_class_name', '_clear_changed_fields', '_collection',
 '_created', '_data', '_db_field_map', '_delta', '_dynamic', '_dynamic_fields',
 '_dynamic_lock', '_fields', '_fields_ordered', '_from_son', '_geo_indices',
 '_get_changed_fields', '_get_collection', '_get_collection_name', '_get_db',
 '_initialised', '_is_base_cls', '_is_document', '_lookup_field',
 '_mark_as_changed', '_meta', '_nestable_types_changed_fields',
 '_object_key', '_qs', '_reload', '_reverse_db_field_map',
 '_subclasses', '_superclasses', '_translate_field_name',
 '_types', '_unique_with_indexes', 'cascade_save',
 'clean', 'compare_indexes', 'delete', 'drop_collection',
 'email', 'ensure_index', 'ensure_indexes', 'first_name',
 'from_json', 'id', 'last_name', 'list_indexes', 'my_metaclass',
 'objects', 'pk', 'register_delete_rule', 'reload', 'save', 'select_related',
 'switch_collection', 'switch_db', 'to_dbref', 'to_json',
 'to_mongo', 'update', 'validate']

o.__dict__:
{'_dynamic_fields': SON([]),
 '_data': {'first_name': 'Ross', 'last_name': 'Lawley',
 'id': ObjectId('548a52d09fa33e476386769a'), 'email': u'ross@example.com'},
 '_changed_fields': [], '_initialised': True, '_created': False}
'''

def db_me_get(M, tid):
    a = M.objects.get(id=tid)
    return a


def db_me_get_all(M):
    a = M.objects.all()
    return a


def db_me_filter(M, *args, **kwargs):
    a = M.objects(**kwargs)
    return a


def db_me_create(M, values):
    a = M(**values)
    a.save()
    return a


def db_me_update(M, oid, values):
    a = db_me_get(M, oid)
    if a:
        a.update(**values)


def db_me_delete(M, oid):
    a = db_me_get(M, oid)
    if a:
        a.delete()


def db_me_delete_all(M):
    a = db_me_get_all(M)
    if a:
        a.delete()


# #### # #### #


def user_get(oid):
    return db_me_get(db_mg.User, oid)


def user_get_all():
    return db_me_get_all(db_mg.User)


def user_filter(*args, **kwargs):
    return db_me_filter(db_mg.User, *args, **kwargs)


def user_create(values):
    return db_me_create(db_mg.User, values)


def user_update(oid, values):
    return db_me_update(db_mg.User, oid, values)


def user_delete(oid):
    return db_me_delete(db_mg.User, oid)


# #### # #### #


def wiki_page_get(oid):
    return db_me_get(db_mg.WikiPage, oid)


def wiki_page_get_all():
    return db_me_get_all(db_mg.WikiPage)


def wiki_page_filter(*args, **kwargs):
    return db_me_filter(db_mg.WikiPage, *args, **kwargs)


def wiki_page_create(values):
    return db_me_create(db_mg.WikiPage, values)


def wiki_page_update(oid, values):
    return db_me_update(db_mg.WikiPage, oid, values)


def wiki_page_delete(oid):
    return db_me_delete(db_mg.WikiPage, oid)
