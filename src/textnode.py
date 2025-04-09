from enum import Enum
from leafnode import LeafNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        return self.text == o.text and self.text_type == o.text_type and self.url == o.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception("invalid text type")

    @staticmethod
    def text_to_textnodes(text):
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = TextNode.split_nodes_image(nodes)
        nodes = TextNode.split_nodes_link(nodes)
        return nodes

    @staticmethod
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for n in old_nodes:
            if n.text_type != TextType.TEXT:
                new_nodes.append(n)
            else:
                if n.text.count(delimiter) % 2 != 0:
                    raise Exception(
                        f"invalid markdown. no matching tag {delimiter}")
                else:
                    strings = n.text.split(delimiter)
                    for idx, s in enumerate(strings):
                        if len(s) > 0:
                            tt = TextType.TEXT if idx % 2 == 0 else text_type
                            s = s.replace("\n", " ")
                            s = re.sub(r"\s+", " ", s)
                            new_nodes.append(TextNode(s, tt))
        return new_nodes

    @staticmethod
    def split_nodes_image(old_nodes):
        new_nodes = []
        for n in old_nodes:
            imgs = TextNode.__extract_markdown_images(n.text)
            if len(imgs) == 0:
                new_nodes.append(n)
            else:
                text = n.text
                for img in imgs:
                    start_idx = text.find(f"![{img[0]}]")
                    s = text[0:start_idx]
                    text = text[start_idx:]
                    if len(s) > 0:
                        new_nodes.append(TextNode(s, TextType.TEXT))

                    new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                    text = text.replace(f"![{img[0]}]({img[1]})", "")

                if len(text) > 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))

        return new_nodes

    @staticmethod
    def split_nodes_link(old_nodes):
        new_nodes = []
        for n in old_nodes:
            links = TextNode.__extract_markdown_links(n.text)
            if len(links) == 0:
                new_nodes.append(n)
            else:
                text = n.text
                for link in links:
                    start_idx = text.find(f"[{link[0]}]")
                    s = text[0:start_idx]
                    text = text[start_idx:]
                    if len(s) > 0:
                        new_nodes.append(TextNode(s, TextType.TEXT))

                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    text = text.replace(f"[{link[0]}]({link[1]})", "")

                if len(text) > 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))

        return new_nodes

    @staticmethod
    def __extract_markdown_images(text):
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches

    @staticmethod
    def __extract_markdown_links(text):
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches
