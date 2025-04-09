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

    @staticmethod
    def block_to_block_type(block_text):
        if Block.__is_heading(block_text):
            return BlockType.HEADING
        if Block.__is_code(block_text):
            return BlockType.CODE
        if Block.__is_quote(block_text):
            return BlockType.QUOTE
        if Block.__is_unordered_list(block_text):
            return BlockType.UNORDERED_LIST
        if Block.__is_ordered_list(block_text):
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH

    @staticmethod
    def __is_heading(block_text):
        if (
            block_text.startswith("# ")
            or block_text.startswith("## ")
            or block_text.startswith("### ")
            or block_text.startswith("#### ")
            or block_text.startswith("##### ")
            or block_text.startswith("###### ")
        ):
            return True
        return False

    @staticmethod
    def __is_code(block_text):
        if block_text.startswith("```") and block_text.endswith("```"):
            return True
        return False

    @staticmethod
    def __is_quote(block_text):
        lines = block_text.split("\n")
        is_quote = True
        for line in lines:
            is_quote = is_quote and line.startswith(">")
        return is_quote

    @staticmethod
    def __is_unordered_list(block_text):
        lines = block_text.split("\n")
        is_list = True
        for line in lines:
            is_list = is_list and line.startswith("- ")
        return is_list

    @staticmethod
    def __is_ordered_list(block_text):
        lines = block_text.split("\n")
        is_list = True
        for idx, line in enumerate(lines):
            is_list = is_list and line.startswith(f"{idx + 1}. ")
        return is_list
