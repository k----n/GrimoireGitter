# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2020 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Nitish Gupta <imnitish.ng@gmail.com>
#

import logging
import re
from urllib.parse import urlparse
import requests

from grimoirelab_toolkit.datetime import str_to_datetime

from .enrich import Enrich, metadata
from ..elastic_mapping import Mapping as BaseMapping


logger = logging.getLogger(__name__)


class Mapping(BaseMapping):

    @staticmethod
    def get_elastic_mappings(es_major):
        """Get Elasticsearch mapping.

        :param es_major: major version of Elasticsearch, as string
        :returns:        dictionary with a key, 'items', with the mapping
        """

        mapping = """
        {
            "properties": {
                "text_analyzed": {
                  "type": "text",
                  "fielddata": true,
                  "index": true
                }
           }
        } """

        return {"items": mapping}


class GitterEnrich(Enrich):

    mapping = Mapping

    # REGEX to extract links from HTML text
    HTML_LINK_REGEX = re.compile("href=[\"\'](.*?)[\"\']")

    def __init__(self, db_sortinghat=None, db_projects_map=None, json_projects_map=None,
                 db_user='', db_password='', db_host=''):
        super().__init__(db_sortinghat, db_projects_map, json_projects_map,
                         db_user, db_password, db_host)

    def get_field_author(self):
        return "fromUser"

    def get_sh_identity(self, item, identity_field=None):
        # email not available for gitter
        identity = {
            'username': None,
            'name': None,
            'email': None
        }

        if self.get_field_author() not in item['data']:
            return identity
        from_ = item['data'][self.get_field_author()]

        identity['username'] = from_.get('username', None)
        identity['name'] = from_.get('displayName', None)

        return identity

    def get_identities(self, item):
        """ Return the identities from an item """

        identity = self.get_sh_identity(item)
        yield identity

    def get_project_repository(self, eitem):
        tokens = eitem['origin'].rsplit("/", 1)
        return tokens[0] + " " + tokens[1]

    @metadata
    def get_rich_item(self, item):

        eitem = {}

        self.copy_raw_fields(self.RAW_FIELDS_COPY, item, eitem)

        message = item['data']

        eitem['unread'] = 1 if message['unread'] else 0
        eitem['text_analyzed'] = message['text']

        copy_fields = ["readBy", "issues", "id"]

        for f in copy_fields:
            if f in message:
                eitem[f] = message[f]
            else:
                eitem[f] = None

        eitem.update(self.get_rich_links(item['data'], item['uuid'], item['origin']))

        message_timestamp = str_to_datetime(eitem['metadata__updated_on'])
        eitem['tz'] = int(message_timestamp.strftime("%H"))

        if self.sortinghat:
            eitem.update(self.get_item_sh(item))

        if self.prjs_map:
            eitem.update(self.get_item_project(eitem))

        eitem.update(self.get_grimoire_fields(item["metadata__updated_on"], "message"))

        self.add_repository_labels(eitem)
        self.add_metadata_filter_raw(eitem)
        return eitem

    def get_rich_links(self, item, uuid, origin):

        rich_item = {}

        if item['issues']:
            self.extract_issues(item['issues'], item['html'], uuid, origin)

        if item['mentions']:
            rich_item['mentioned'] = self.extract_mentions(item['mentions'])

        rich_item['url_hostname'] = []

        if item['urls']:
            for url in item['urls']:
                try:
                    url_parsed = urlparse(url['url'])
                    rich_item['url_hostname'].append('{uri.scheme}://{uri.netloc}/'.format(uri=url_parsed))
                except ValueError: # url could not be properly parsed
                    logger.error("[gitter] UUID {} - Could not parse URL '{}'".format(uuid, url))
                    continue

        return rich_item

    def extract_issues(self, issue_pr, html_text, uuid, origin):
        """Enrich issues or PRs mentioned in the message"""

        project_repo = '/'.join(origin.split("/")[-2:]).lower()

        links_found = self.HTML_LINK_REGEX.findall(html_text)
        for i, entity in enumerate(issue_pr):
            # Determine the kind of repo that the message refers to
            if 'repo' in entity.keys():
                r = entity['repo'].lower()
                if r == project_repo:
                    repo_type = 'project'
                elif r.split('/')[0] == project_repo.split('/')[0]:
                    repo_type = 'parent'
                else:
                    repo_type = 'foreign'

            # First check to see if issue could be determined via parsed html link
            if 'repo' in entity.keys() and 'number' in entity.keys() and links_found:
                try:
                    if links_found[i].split('/')[-2] == 'issues':
                        entity['is_issue'] = entity['repo'] + ' #' + entity['number']
                    elif links_found[i].split('/')[-2] == 'pull':
                        entity['is_pull'] = entity['repo'] + ' #' + entity['number']
                    else:
                        continue
                    entity['url'] = links_found[i]
                    entity['repo_type'] = repo_type
                    continue
                except IndexError:
                    pass
            
            # If issue is referred to in a span tag, then we will need to connect to github
            # to determine if the issue is a pull request or issue
            if 'repo' in entity.keys() and 'number' in entity.keys():
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                url = 'https://github.com/' + entity['repo'] + '/issues/' + entity['number']
                response = requests.get(url, headers=headers)

                # Check to see if it is a redirect, then it is probably a pull request
                if response.history:
                    entity['is_pull'] = entity['repo'] + ' #' + entity['number']
                    entity['url'] = 'https://github.com/' + entity['repo'] + '/pull/' + entity['number']
                    entity['repo_type'] = repo_type
                elif response.status_code == 200:
                    entity['is_issue'] = entity['repo'] + ' #' + entity['number']
                    entity['url'] = url
                    entity['repo_type'] = repo_type
                
                continue

            logger.error("[gitter] UUID {} - Could not resolve issue with index {}".format(uuid, i))

    def extract_mentions(self, mentioned):
        """Enrich users mentioned in the message"""

        rich_mentions = []

        for usr in mentioned:
            if 'userId' in usr.keys():
                rich_mentions.append({'mentioned_username': usr['screenName'], 'mentioned_userId': usr['userId']})

        return rich_mentions

