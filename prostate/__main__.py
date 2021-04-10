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
import os
import pkg_resources
from typing import Dict

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

    def _get_cookies(self) -> Dict[str, str]:
        cookie_model = self.builder.get_object("req-cookies-model")
        return {c[0]: c[1] for c in cookie_model}

    def _display_response(self, response: Response):
        resp_text = f"HTTP {response.status_code} {response.reason}\n"

        for k, v in response.headers.items():
            resp_text += f"{k}: {v}\n"
        resp_text += "\n"
        resp_text += response.content.decode("utf8")

        self.response_buffer.set_text(resp_text)

    def on_request_send(self, _):
        method = self._get_selected_method()
        url_input = self.builder.get_object("req-input-url")
        url = url_input.get_text().strip()
        if not self.http_client.is_valid_url(url):
            print("URL is not valid!")
            return

        cookies = self._get_cookies()
        response = self.http_client.send(method=method, url=url, cookies=cookies)
        self._display_response(response)

    def on_request_menu_cookies_activated(self, _):
        cookie_box = self.builder.get_object("req-cookies-window")
        cookie_box.show_all()

    def on_req_cookies_window_close(self, *_):
        cookie_box = self.builder.get_object("req-cookies-window")
        cookie_box.hide()

        # Clear any unset cookies
        cookie_model = self.builder.get_object("req-cookies-model")
        for cookie in cookie_model:
            if cookie[0] is None or cookie[0].strip() == "":
                cookie_model.remove(cookie.iter)

        return True

    def on_req_cookie_add(self, *_):
        cookie_model = self.builder.get_object("req-cookies-model")
        cookie_model.append()

    def on_req_cookie_delete(self, *_):
        selection = self.builder.get_object("req-cookies-selection")
        model, iter = selection.get_selected()
        if iter is None:
            return
        model.remove(iter)

    def on_req_cookie_clear(self, *_):
        cookie_model = self.builder.get_object("req-cookies-model")
        cookie_model.clear()

    def on_req_cookie_edited_name(self, _, path, value):
        cookie_model = self.builder.get_object("req-cookies-model")
        cookie_model[path][0] = str(value)

    def on_req_cookie_edited_value(self, _, path, value):
        cookie_model = self.builder.get_object("req-cookies-model")
        cookie_model[path][1] = str(value)

    def on_req_cookie_added(self, store, path, iter):
        self.builder.get_object("req-cookies-btn-clear").set_sensitive(True)

    def on_req_cookie_deleted(self, store, *_):
        if store.iter_n_children() == 0:
            self.builder.get_object("req-cookies-btn-clear").set_sensitive(False)

    def on_req_cookie_selected(self, selection):
        model, iter = selection.get_selected()
        if iter is None:
            self.builder.get_object("req-cookies-btn-delete").set_sensitive(False)
        else:
            self.builder.get_object("req-cookies-btn-delete").set_sensitive(True)

    @staticmethod
    def on_app_window_destroy(_):
        Gtk.main_quit()


def main():
    gui_file = pkg_resources.resource_filename(
        __package__, os.path.join("ui", "prostate.glade")
    )
    controller = GuiController(gui_file, HTTPClient())
    controller.main_window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
