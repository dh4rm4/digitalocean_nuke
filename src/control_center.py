#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parameterized import parameterized
from typing import NoReturn

from execution_transparency import execution_transparency
from spaces.spaces_eraser import spaces_eraser
from generic.generic_eraser import generic_eraser


class control_center(execution_transparency):
    """
        Core methods to nuke DigitalOcean ressources
    """
    def start_end_of_time(self) -> bool:
        """
            Main function to start destroying all
            digitalOcean ressources.
                return: (bool) True if one ressource
                               destruction failed
        """
        for method_name in self.dynamic_methods():
            getattr(self, method_name)()

    def dynamic_methods(self):
        """
            Return all dynamically generated methods used
            to destroy ressources
        """
        for method_name in dir(self):
            if 'destroy_ressources_' in method_name:
                yield method_name

    @parameterized.expand([
        ['nuke_droplets', generic_eraser, 'get_all_droplets'],
        ['nuke_firewalls', generic_eraser, 'get_all_firewalls'],
        ['nuke_load_balancers', generic_eraser, 'get_all_load_balancers'],
        ['nuke_certificates', generic_eraser, 'get_all_certificates'],
        ['nuke_volumes', generic_eraser, 'get_all_volumes'],
        ['nuke_snapshots', generic_eraser, 'get_all_snapshots'],
        ['nuke_spaces', spaces_eraser, None],
    ])
    def destroy_ressources(self, f_name: str,
                           class_name, method_name: str) -> NoReturn:
        """
            Uses DO-API wrapper to nuke given ressources
                - param0: (str) name of the ressource
                - param1: (class) name of the class use to destroy
                                given ressource
                - param2: (str) method name uses by the wrapper
                                to fetch all given ressources
        """
        try:
            class_name().launch_nuke(method_name)
            self._print_ok(f_name)
        except Exception:
            self._ko(f_name)


if __name__ in '__main__':
    with control_center() as instance:
        instance.start_end_of_time()
