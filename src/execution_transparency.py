#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getenv
import logging
from typing import NoReturn


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
        """
            This magic method makes the Gitlab's job fail,
            if one nuke missed its target.
        """
        if self.did_pipeline_failed is True:
            err_msg = 'One nuke missed his target.\n' \
                      '\tSee the log file artifact for more details'
            raise Exception(err_msg)

    def _print_ok(self, func_name: str) -> NoReturn:
        """
            Outputs destruction status as OK
        """
        print(func_name, end=':\t')
        print('\033[92mOK\033[0m')

    def _ko(self, func_name: str) -> NoReturn:
        """
           Manage error transparency after a ressource
           destruction failed
               a. set pipeline as failed
               b. log exception in log gile
               c. output destruction status as KO
        """
        self.did_pipeline_failed = True
        self._log_error(func_name)
        self._print_ko(func_name)

    def _print_ko(self, func_name: str) -> NoReturn:
        """
            Outputs destruction status as KO
        """
        print(func_name, end=':\t')
        print('\033[91mKO\033[0m')

    def _log_error(self, f_name: str):
        """
            Log all exception raised during ressources destruction
            in the file error_logs_${CI_COMMIT_SHA}.txt
        """
        err_msg = 'Exception occured during "{0}" method ' \
                  'execution'.format(f_name)
        logging.exception(err_msg)
