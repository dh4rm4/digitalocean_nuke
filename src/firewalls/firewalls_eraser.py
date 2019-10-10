#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generic.generic_eraser import generic_eraser


class firewalls_eraser(generic_eraser):
    def launch_nuke(self):
        for firewalls in self.do_client.get_all_firewalls():
            self._delete_ressource(firewalls)
