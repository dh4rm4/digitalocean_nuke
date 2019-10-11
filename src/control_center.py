#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getenv
import logging
from parameterized import parameterized
from typing import NoReturn

from spaces.spaces_eraser import spaces_eraser
from generic.generic_eraser import generic_eraser


COMMIT_SHA = getenv('CI_COMMIT_SHA', 'ERROR_NO_VAR')
LOG_FILENAME = 'error_logs_' + COMMIT_SHA + '.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)


class execution_transparency:
    """
        Contain all methods used to manage pipeline state
        + output execution status
        + error logging
    """
    did_pipeline_failed: bool = False

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.did_pipeline_failed is True:
            err_msg = 'One nuke missed his target.\n' \
                      '\tSee the log file artifact for more details'
            raise Exception(err_msg)

    def _print_ok(self, func_name: str) -> NoReturn:
        print(func_name, end=':\t')
        print('\033[92mOK\033[0m')

    def _ko(self, func_name: str) -> NoReturn:
        self.did_pipeline_failed = True
        self._log_error(func_name)
        self._print_ko(func_name)

    def _print_ko(self, func_name: str) -> NoReturn:
        print(func_name, end=':\t')
        print('\033[91mKO\033[0m')

    def _log_error(self, f_name: str):
        err_msg = 'Exception occured during "{0}" method ' \
                  'execution'.format(f_name)
        logging.exception(err_msg)


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
        self.destroy_ressources_0_nuke_droplets()
        self.destroy_ressources_1_nuke_firewalls()
        self.destroy_ressources_2_nuke_load_balancers()
        self.destroy_ressources_3_nuke_certificates()
        self.destroy_ressources_4_nuke_volumes()
        self.destroy_ressources_5_nuke_snapshots()
        self.destroy_ressources_6_nuke_spaces()

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
