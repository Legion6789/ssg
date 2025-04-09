from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class Block:
    @staticmethod
    def markdown_to_blocks(markdown):
        blocks = []
        for b in markdown.split("\n\n"):
            b = b.strip()
            b = b.replace("            ", "")
            if len(b) > 0:
                blocks.append(b)

        return blocks
