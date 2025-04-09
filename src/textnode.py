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
                return LeafNode("`", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception("invalid text type")

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
                            new_nodes.append(TextNode(s, tt))
        return new_nodes

    @staticmethod
    def extract_markdown_images(text):
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches

    @staticmethod
    def extract_markdown_links(text):
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return matches
