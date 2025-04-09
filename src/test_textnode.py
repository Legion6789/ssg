import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text nod", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is not a link node", TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_url_not_none(self):
        node = TextNode("This is not a link node",
                        TextType.LINK, "https://google.com")
        self.assertEqual(node.url, "https://google.com")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_code_first(self):
        node = TextNode("`This is the code block` this is text", TextType.TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is the code block")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " this is text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_split_two_code_blocks_first(self):
        node = TextNode("`code block` text `code block`", TextType.TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "code block")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " text ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "code block")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = TextNode.split_nodes_delimiter(
            [node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        matches = TextNode.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_two_images(self):
        matches = TextNode.extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = TextNode.extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
