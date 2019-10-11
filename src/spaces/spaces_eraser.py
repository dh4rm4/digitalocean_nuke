#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module to nuke all Spaces (=buckets)
    from a given DigitalOcean account
"""

import boto3
from os import getenv
from typing import List
import datetime
import pytz


class spaces_eraser:
    """
        Class used to list then destroy all digitalocean
        spaces (=bucket) in every available region
    """
    region_tags = ['fra1', 'nyc3', 'sfo2', 'sgp1', 'ams3']

    def __init__(self):
        """
            The following environnement variables need to be define:
                - DO_VAR_SPACES_ACCESS_ID: DO Space access id
                - DO_VAR_SPACES_ACCESS_KEY: DO Space access key
                - DO_VAR_RSRC_TIMEOUT: max lifetime for ressources in seconds
        """
        self.SPACE_ACCESS_ID = getenv('DO_VAR_SPACES_ACCESS_ID',
                                      'ERROR_MISSING_VAR')
        self.SPACE_ACCESS_KEY = getenv('DO_VAR_SPACES_ACCESS_KEY',
                                       'ERROR_MISSING_VAR')
        self.RSRC_TIMEOUT = int(getenv('DO_VAR_RSRC_TIMEOUT',
                                       'ERROR_MISSING_VAR'))

    def launch_nuke(self):
        """
            Entrypoint to nuke all account's spaces
        """
        for region_tag in self.region_tags:
            self.delete_all_spaces(region_tag)

    def delete_all_spaces(self, region_tag: str):
        """
            Delete all spaces and their contents of the given
            datacenter
                - param0: (str) datacenter's region tag
        """
        self.s3_client = self.init_space_connection(region_tag)
        for space in self.get_space_list():
            self.delete_space(space)
        del self.s3_client

    def init_space_connection(self, region_tag: str):
        """
            Init a connection with DO Spaces Api server,
            and return the built object
                - param0: (str) datacenter region tag
        """
        session = boto3.session.Session()
        space_url = 'https://' + \
                    str(region_tag) + \
                    '.digitaloceanspaces.com'
        client = session.client('s3', region_name=region_tag,
                                endpoint_url=space_url,
                                aws_access_key_id=self.SPACE_ACCESS_ID,
                                aws_secret_access_key=self.SPACE_ACCESS_KEY)
        return client

    def get_space_list(self) -> List:
        """
            Build and return a list of all the spaces' name
            using the DO Api server connection object
        """
        spaces = self.s3_client.list_buckets()
        spaces_names = []
        for bucket in spaces['Buckets']:
            if self._idle_space(bucket):
                spaces_names.append(bucket['Name'])
        return spaces_names

    def _idle_space(self, bucket: dict):
        """
            Check if given bucket is old enough to be deleted
                - param0: (dict) bucket's infos dictionnary
        """
        current_date = pytz.timezone('UTC').localize(datetime.datetime.now())
        bucket_creation_date = bucket['CreationDate']
        lifetime = current_date - bucket_creation_date
        return lifetime.total_seconds() > self.RSRC_TIMEOUT

    def delete_space(self, space_name: str):
        """
            Uses s3 session object to delete the given
            space content and itself
                - param0: (str) space's name
        """
        self.delete_space_content(space_name)
        try:
            self.s3_client.delete_bucket(Bucket=space_name)
        except boto3.exceptions.S3UploadFailedError:
            pass

    def delete_space_content(self, space_name: str):
        """
            Uses s3 session object to list all objects in given space.
            Doing so 1000 items as a time
                - param0: (str) space's name
        """
        space_objects = self.s3_client.list_objects(Bucket=space_name)
        try:
            self.delete_objects(space_name, space_objects['Contents'])
            if len(space_objects['Contents']) > 999:
                self.delete_space_content(space_name)
        except KeyError:
            pass

    def delete_objects(self, space_name: str, spaces_objects):
        """
            Delete all given objects from the space, one a time
                - param0: (str) space's name
                - param1: (list) list object from botocore.client.S3.list_objects
        """
        for obj in spaces_objects:
            self.s3_client.delete_object(Bucket=space_name,
                                         Key=obj['Key'])
