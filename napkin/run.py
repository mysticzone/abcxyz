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
Run a simple flask web for test,

    python run.py

"""

import os
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

sys.path.insert(0, BASE_DIR)


from napkin.app import app
from napkin.statics import static_file

app._static_folder = os.path.join(BASE_DIR, 'static')

app = static_file.app_load_static_file(app)


if __name__ == "__main__":
    port = 8009
    app.debug = True
    app.run(host='0.0.0.0', port=port)
