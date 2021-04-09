# -*- coding: utf8 -*-
# ----------------------------------------------------------------------------
# Prostate - HTTP Testing Tool
# Copyright (C) 2021 Shahar Evron
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
"""HTTP client and utils for Prostate
"""
import requests


class HTTPClient:

    def __init__(self):
        self.sess = requests.Session()

    def send(self, method: str, url: str):
        req = requests.Request(method=method, url=url)
        resp = self.sess.send(req.prepare())
        return resp