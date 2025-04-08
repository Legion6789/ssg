import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_no_props(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_href_props(self):
        node = HtmlNode(
            None, None, None, {
                "href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_img_props(self):
        node = HtmlNode(
            None,
            None,
            None,
            {"src": "https://www.google.com/img.jpg", "alt": "alt text"},
        )
        self.assertEqual(
            node.props_to_html(), ' src="https://www.google.com/img.jpg" alt="alt text"'
        )


if __name__ == "__main__":
    unittest.main()
