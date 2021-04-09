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

import pkg_resources
from os import path

from requests import Response

from .gtkwrapper import Gtk
from .http import HTTPClient


class GuiController:
    """GUI Controller"""

    def __init__(self, glade_file: str, http_client: HTTPClient):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.main_window: Gtk.ApplicationWindow = self.builder.get_object("app-window")
        self.response_buffer: Gtk.TextBuffer = self.builder.get_object(
            "response-buffer"
        )
        self.builder.connect_signals(self)

        self.http_client = http_client

    def _get_selected_method(self):
        combo = self.builder.get_object("req-input-method")
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            method = model[tree_iter][0]
            return method
        else:
            return combo.get_child()

    def _display_response(self, response: Response):
        resp_text = f"HTTP {response.status_code} {response.reason}\n"

        for k, v in response.headers.items():
            resp_text += f"{k}: {v}\n"
        resp_text += "\n"
        resp_text += response.content.decode("utf8")

        self.response_buffer.set_text(resp_text)

    def on_request_send(self, _):
        method = self._get_selected_method()
        url = self.builder.get_object("req-input-url").get_text().strip()
        response = self.http_client.send(method=method, url=url)
        self._display_response(response)

    @staticmethod
    def on_app_window_destroy(_):
        Gtk.main_quit()


def main():
    gui_file = pkg_resources.resource_filename(
        __package__, path.join("ui", "prostate.glade")
    )
    controller = GuiController(gui_file, HTTPClient())
    controller.main_window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
