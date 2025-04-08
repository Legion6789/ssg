from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag cannot be None")
        if self.children is None:
            raise ValueError("children cannot be None")

        s = f"<{self.tag}>"
        for c in self.children:
            s += c.to_html()
        s += f"</{self.tag}>"
        return s
