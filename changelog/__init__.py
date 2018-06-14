#
# Copyright (C) 2017 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import absolute_import
from changelog.gerrit import GerritServer, datetime_to_gerrit
from requests.exceptions import ConnectionError

from datetime import datetime, timedelta

import json
import requests
import re

with open('device_deps.json') as f:
    dependencies = json.load(f)

def is_related_change(gerrit, device, curbranch, project, branch):

    if device == "all":
        return True

    if device not in dependencies:
        return True

    deps = dependencies[device]
    for dep in deps:
        return dep == project

    return False

def get_timestamp(ts):
    if not ts:
        return None
    return int((ts - datetime(1970, 1, 1)).total_seconds())

def get_changes(gerrit, device=None, before=-1, version='8.1', status_url='#'):
    last_release = -1

    query = 'status:merged'
    if last_release != -1:
        query += ' after:' + datetime_to_gerrit(last_release)
    if before != -1:
        query += ' before:' + datetime_to_gerrit(datetime.fromtimestamp(before))

    changes = gerrit.changes(query=query, n=100, limit=100)

    nightly_changes = []
    last = 0
    try:
        for c in changes:
            last = get_timestamp(c.updated)
            if is_related_change(gerrit, device, version, c.project, c.branch):
                nightly_changes.append({
                    'project': c.project,
                    'subject': c.subject,
                    'submitted': get_timestamp(c.submitted),
                    'updated': get_timestamp(c.updated),
                    'url': c.url,
                    'owner': c.owner
                })
    except ConnectionError as e:
        print(e)
        nightly_changes.append({
            'project': None,
            'subject': None,
            'submitted': 0,
            'updated': 0,
            'url': status_url,
            'owner': None
            })
    return {'last': last, 'res': nightly_changes }
