import unittest

from instasteem.parser import InstagramPostParser
from instasteem.sync import Sync

TEST_POST = "https://www.instagram.com/p/BsfudqQgGlw/"

class IntegrationTest(unittest.TestCase):

    def test_image_parsing(self):
        p = InstagramPostParser(TEST_POST)
        images = p.extract_images()
        self.assertEqual(len(images), 2)
        self.assertIn(
            "https://instagram.fist1-1.fna.fbcdn.net/vp/0cd84e674b90ee4c4e98bd"
            "efcaade34c/5CB71FF4/t51.2885-15/e35/47694741_544033789434599_2325"
            "102288486633689_n.jpg?_nc_ht=instagram.fist1-1.fna.fbcdn.net",
            images
        )

    def test_metadata_parsing(self):
        p = InstagramPostParser(TEST_POST)
        metadata = p.extract_metadata()
        self.assertEqual(len(metadata), 4)
        self.assertEqual("Hamburg, Germany", metadata[0])
        self.assertEqual(
            "lorem Ipsum is simply dummy text of the printing and typesettin"
            "g industry. Lorem Ipsum has been the industry&#x27;s standard "
            "dummy text ever since the 1500s, when an unknown printer took "
            "a galley of type and scrambled it to make a type specimen book. "
            "It has survived not only five centuries, but also the leap into"
            " electronic typesetting, remaining essentially unchanged."
            " It was popularised in the 1960s with the release of Letraset "
            "sheets containing Lorem Ipsum passages, and more recently with"
            " desktop publishing software like Aldus PageMaker including "
            "versions of Lorem Ipsum.",
        metadata[1]
        )
        self.assertEqual(
            "instasteem on Instagram: “lorem Ipsum is simply "
                         "dummy text of the printing and typesetting industry."
                         " Lorem Ipsum has been the industry's standard dummy "
                         "text ever…”",
            metadata[2],
        )
        self.assertEqual("2019-01-11T13:20:03", metadata[3])

class ParserTest(unittest.TestCase):

    def test_invalid_url(self):
        with self.assertRaises(ValueError) as context:
            InstagramPostParser("http://invaliddomain.org")

    def test_injection(self):
        p = InstagramPostParser(TEST_POST)
        self.assertNotEqual(None, p.content)

class SyncTest(unittest.TestCase):

    def test_client_keys(self):
        s = Sync(keys=["foo"])
        self.assertEqual(s.client.keys, ["foo",])

    def test_post(self):
        s = Sync()
        op = s.post("foo", "title", "body", ["tag1", "tag2"], safe_mode=True)
        self.assertEqual(op.op_id, "comment")
        self.assertEqual(op.op_data["parent_author"], None)
        self.assertEqual(op.op_data["parent_permlink"], "tag1")
        self.assertEqual(op.op_data["author"], "foo")
        self.assertEqual(op.op_data["permlink"], "title")
        self.assertEqual(op.op_data["title"], "title")

if __name__ == '__main__':
    unittest.main()