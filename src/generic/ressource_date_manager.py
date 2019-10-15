#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import pytz


class ressource_date_manager:
    """
        Manage the difference between given date and
        'now' using timezone
    """
    def __init__(self, *args, **kwargs):
        """
            - timezone: (str) timezone of the ressource's date
            - created_at: (str) string containing the date
                          (datetime) datetime object containing
                                     the creation date
            - date_format: (str) date format used to init
                                 datetime operations
        """
        self.now = self.build_current_date()
        self.created_at = self.build_creation_date(kwargs.get('timezone',
                                                              None),
                                                   kwargs.get('created_at',
                                                              None),
                                                   kwargs.get('date_format',
                                                              None))

    def build_creation_date(self, timezone: str,
                            created_at,
                            date_format: str):
        """
            Convert given infos into a datetime object.
            (Return created_at var if it's a datetime object)
            - timezone: (str) timezone of the ressource's date
            - created_at: (str) string containing the date
                          (datetime) datetime object containing
                                     the creation date
            - date_format: (str) date format used to init
                                 datetime operations
        """
        if not isinstance(created_at, str):
            return created_at
        tz = pytz.timezone(timezone)
        return tz.localize(datetime.strptime(created_at,
                                             date_format))

    def build_current_date(self):
        tz = pytz.timezone('Europe/Paris')
        return tz.localize(datetime.now())

    def is_idle(self, ressource_timeout):
        """
            Return a bool based on the difference between 'now'
            and the given creation_date compare to given timeout
        """
        lifetime = self.now - self.created_at
        return lifetime.total_seconds() > ressource_timeout
