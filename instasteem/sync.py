import json

from lightsteem.client import Client
from lightsteem.datastructures import Operation
from slugify import slugify


class Sync:

    def __init__(self, client=None, keys=None):
        self.client = client or Client(keys=keys)

    def post(self, username, title, body, tags, safe_mode=False):
        """Sync the parsed post into the STEEM blockchain.

        :param username: Author on STEEM blockchain
        :param title: Title on the STEEM post
        :param body: Body of the post
        :param tags: A list of tags
        """
        post = Operation('comment', {
            "parent_author": None,
            "parent_permlink": tags[0],
            "author": username,
            "permlink": slugify(title),
            "title": title,
            "body": body,
            "json_metadata": json.dumps({"tags": tags})
        })
        if safe_mode:
            return post
        else:
            self.client.broadcast(post)