#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getenv
from datetime import datetime
import digitalocean as do
import pytz


class generic_eraser:
    """
        Main DigitalOcean ressources eraser.
        It uses the API Wrapper python-digitalocean:
        https://github.com/koalalorenzo/python-digitalocean
    """
    def __init__(self):
        """
            The following environnement variables need to be define:
                - DO_VAR_RSRC_TIMEOUT: max lifetime of a ressource
                                        (in seconds)
                - DO_VAR_TOKEN: main digitalocean token
        """
        self.RSRC_TIMEOUT = int(getenv('DO_VAR_RSRC_TIMEOUT',
                                       'ERROR_MISSING_VAR'))
        self.DO_TOKEN = getenv('DO_VAR_TOKEN',
                               'MISSING_DO_TOKEN_VAR')
        self.do_client = do.Manager(token=self.DO_TOKEN)

    def launch_nuke(self, method_name):
        """
            Starting point to nuke a given ressource.
                - param0: (str) method name specific to the ressource to nuke
        """
        for ressource in getattr(self.do_client, method_name)():
            self._delete_ressource(ressource)

    def _delete_ressource(self, ressource):
        """
            Delete given ressource if lifetime is higher
            than the ressource timout set
                - param0: ressource objects
        """
        if self._idle_ressource(ressource):
            ressource.destroy()

    def _idle_ressource(self, ressource):
        """
            Check if given ressource is old enough to be deleted
                - param0: ressource objects
        """
        tz = pytz.timezone('UTC')
        creation_date = tz.localize(datetime.strptime(ressource.created_at,
                                                      '%Y-%m-%dT%H:%M:%SZ'))
        tz = pytz.timezone('Europe/Paris')
        current_date = tz.localize(datetime.now())
        lifetime = current_date - creation_date
        return lifetime.total_seconds() > self.RSRC_TIMEOUT
