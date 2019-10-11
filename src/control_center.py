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


class control_center:
    did_pipeline_failed: bool = False

    def start_end_of_time(self) -> bool:
        """
            Main function to start destroying all
            digitalOcean ressources.
                return: (bool) True if one ressource
                               destruction failed
        """
        self.nuke_spaces()
        self.destroy_ressources_0_nuke_droplets()
        self.destroy_ressources_1_nuke_firewalls()
        self.destroy_ressources_2_nuke_load_balancers()
        self.destroy_ressources_3_nuke_certificates()
        self.destroy_ressources_4_nuke_volumes()
        self.destroy_ressources_5_nuke_snapshots()
        return self.did_pipeline_failed

    def nuke_spaces(self):
        """
            Start the nuke of all DigitialOcean Spaces
        """
        try:
            spaces_eraser().launch_nuke()
            self._print_ok('nuke_spaces')
        except Exception:
            self._ko('nuke_spaces')

    @parameterized.expand([
        ['nuke_droplets', 'get_all_droplets'],
        ['nuke_firewalls', 'get_all_firewalls'],
        ['nuke_load_balancers', 'get_all_load_balancers'],
        ['nuke_certificates', 'get_all_certificates'],
        ['nuke_volumes', 'get_all_volumes'],
        ['nuke_snapshots', 'get_all_snapshots'],
    ])
    def destroy_ressources(self, f_name: str, method_name: str) -> NoReturn:
        """
            Uses DO-API wrapper to nuke given ressources
                - param0: (str) name of the ressource
                - param1: (str) method name uses by the wrapper
                                to fetch all given ressources
        """
        try:
            generic_eraser().launch_nuke(method_name)
            self._print_ok(f_name)
        except Exception:
            self._ko(f_name)

    def _print_ok(self, func_name: str) -> NoReturn:
        print(func_name, end=':\t')
        print('\033[92mOK\033[0m')

    def _ko(self, func_name: str) -> NoReturn:
        self.did_pipeline_failed = True
        self._log_error(func_name)
        print(func_name, end=':\t')
        print('\033[91mKO\033[0m')

    def _log_error(self, f_name: str):
        err_msg = 'Exception occured during "{0}" method ' \
                  'execution'.format(f_name)
        logging.exception(err_msg)


if __name__ in '__main__':
    failed = control_center().start_end_of_time()
    if failed is True:
        err_msg = 'One nuke missed his target.\n' \
                  '\tSee the log file artifact for more details'
        raise Exception(err_msg)
