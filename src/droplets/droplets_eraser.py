#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getenv
from datetime import datetime
import digitalocean as do
import pytz


class droplets_eraser:
    def __init__(self):
        self.RSRC_TIMEOUT = int(getenv('DO_VAR_RSRC_TIMEOUT',
                                       'ERROR_MISSING_VAR'))
        self.DO_TOKEN = getenv('DO_VAR_TOKEN',
                               'MISSING_DO_TOKEN_VAR')
        self.do_client = do.Manager(token=self.DO_TOKEN)

    def launch_nuke(self):
        for droplet in self.do_client.get_all_droplets():
            self._delete_droplet(droplet)

    def _delete_droplet(self, droplet):
        """
            Delete given droplet if lifetime is higher
            than the ressource timout set
                - param0: droplet objects
        """
        if self._idle_droplet(droplet):
            droplet.destroy()

    def _idle_droplet(self, droplet):
        """
            Check if given droplet is old enough to be deleted
                - param0: droplet objects
        """
        tz = pytz.timezone('UTC')
        creation_date = tz.localize(datetime.strptime(droplet.created_at,
                                                      '%Y-%m-%dT%H:%M:%SZ'))
        current_date = tz.localize(datetime.now())
        lifetime = current_date - creation_date
        return lifetime.total_seconds() > self.RSRC_TIMEOUT
