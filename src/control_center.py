#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spaces.spaces_eraser import spaces_eraser
import logging
from parameterized import parameterized
from typing import NoReturn


LOG_FILENAME = 'error_logs.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)


class control_center:
    def start_end_of_time(self):
        self.generic_0_nuke_spaces()

    @parameterized.expand([
        ['nuke_spaces', spaces_eraser]
    ])
    def generic(self, f_name: str, curr_class) -> NoReturn:
        try:
            curr_class().launch_nuke()
            self._print_ok(f_name)
        except Exception:
            err_msg = 'Exception occured during "{0}" method ' \
                      'execution'.format(f_name)
            logging.exception(err_msg)
            self._print_ko(f_name)

    def _print_ok(self, func_name: str) -> NoReturn:
        print(func_name, end=':\t')
        print('\033[92mOK\033[0m')

    def _print_ko(self, func_name: str) -> NoReturn:
        print(func_name, end=':\t')
        print('\033[91mKO\033[0m')


if __name__ in '__main__':
    control_center().start_end_of_time()
