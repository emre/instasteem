import os
import sys

import click

from .parser import InstagramPostParser
from .post_template import get_body
from .sync import Sync


@click.command()
@click.argument('url')
@click.option(
    '--steem-username',
    required=False,
    help='STEEM username')
@click.option(
    '--tags',
    required=False,
    help="Tags",
)
@click.option(
    '--include-metadata',
    required=False,
    default=False,
    help="Include metadata table"
)
def post(url, steem_username=None, tags=None, include_metadata=None):
    """Sync instagram posts to your STEEM account"""
    tag_list = []
    if tags:
        tag_list = tags.split(",")
    else:
        tag_list = ["photography", ]

    parser = InstagramPostParser(url)
    metadata = parser.extract_metadata()
    if not metadata:
        click.echo("Couldn't fetch the metadata.", err=True)
        sys.exit()
    images = parser.extract_images()
    if not len(images):
        click.echo("Couldn't fetch the image(s).", err=True)
        sys.exit()
    location, description, name, upload_date = metadata

    # get the post body
    body = get_body(
        images, location, description, parser.url, upload_date,
        include_metadata=include_metadata)

    if os.environ.get("INSTASTEEM_POSTING_KEY") and steem_username:
        # If posting_key and steem_username is given,
        # directly post to the blockchain without the manual touch
        sync = Sync(keys=[os.environ.get("INSTASTEEM_POSTING_KEY")])
        sync.post(
            steem_username,
            name,
            body,
            tag_list
        )
        click.echo("Broadcasted the post. Check your profile.")
    else:
        # Just parse the body and return
        # We don't have steem user credentials.
        click.echo(body)


def main():
    post()
