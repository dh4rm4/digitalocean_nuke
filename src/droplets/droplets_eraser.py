#!/usr/bin/env python
# -*- coding: utf-8 -*-

from generic.generic_eraser import generic_eraser


class droplets_eraser(generic_eraser):
    def launch_nuke(self):
        for droplets in self.do_client.get_all_droplets():
            self._delete_ressource(droplets)
