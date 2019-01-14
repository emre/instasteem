import requests
import re
import json
import html

# faking user agent to make sure instagram thinks that's a normal request
headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
        ' Safari/537.36'
}


class InstagramPostParser:

    def __init__(self, url):
        self.url = url
        self.content = None
        self.inject_post()

    def inject_post(self):
        """ Injects related instagram post's HTML content into self.content.

        :return (InstagramPostParser): self
        """
        if 'instagram.com' not in self.url:
            raise ValueError("Invalid URL")
        r = requests.get(self.url, headers=headers)
        self.content = r.text

        return self

    def extract_images(self, content=None):
        """Extracts image urls from an Instagram post.

        :param content: (str): HTML content of the post.
        :return (list): A list of image urls
        """
        content = content or self.content
        images = re.findall('{"src":"(.*?)"', content)
        original_images = set()
        for image in images:
            # skip the thumbnails
            if '640x640' in image or '750x750' in image:
                continue
            original_images.add(image)

        return original_images

    def extract_metadata(self, content=None):
        """Return caption and location info of the Instagram post

        :param content: (str): HTML content of the post.
        :return: (tuple): Location name and caption and name
        """
        content = content or self.content
        metadata_info = re.search(
            '<script type="application\/ld\+json">(.*?)</script>',
            content,
            flags=re.MULTILINE | re.DOTALL)
        if metadata_info:
            metadata = json.loads(metadata_info.group(1))
            return metadata["contentLocation"]["name"], \
                   metadata["caption"], \
                   html.unescape(metadata["name"]), \
                   metadata["uploadDate"]