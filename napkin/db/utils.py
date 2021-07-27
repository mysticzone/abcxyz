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

from napkin.db import api as db_api


def node_get_one_by_roles(rls):
    ns = db_api.node_filter(role_ids=rls)
    if len(ns) > 0:
        return ns[0]
    else:
        return None


def node_info_get_by_hostname(hostname):
    nis = db_api.node_info_filter(name=hostname)
    if len(nis) > 0:
        return nis[0]
    else:
        return None


def node_info_ips_from_nics(node_info):
    nics = node_info.nics
    ips = []
    for nic, inets in nics.items():
        if 'address' in inets.keys():
            ips.append(inets['address'])
    return ips

