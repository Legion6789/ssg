import unittest
import textwrap

from nodehelper import NodeHelper


class TestHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """)

        node = NodeHelper.markdown_to_html_node(md)
        html = node.to_html()
        # print("===HTML===")
        # print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """)

        node = NodeHelper.markdown_to_html_node(md)
        html = node.to_html()
        # print("===HTML===")
        # print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
