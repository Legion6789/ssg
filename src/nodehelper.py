from parentnode import ParentNode
from leafnode import LeafNode
from block import BlockType, Block
from textnode import TextNode


class NodeHelper:
    @staticmethod
    def markdown_to_html_node(markdown):
        parent = ParentNode("div", None, None)
        children = []
        blocks = Block.markdown_to_blocks(markdown)
        for b in blocks:
            b_type = Block.block_to_block_type(b)
            match b_type:
                case BlockType.HEADING:
                    children.append(NodeHelper.__heading_block_to_html_node(b))
                case BlockType.CODE:
                    children.append(NodeHelper.__code_block_to_html_node(b))
                case BlockType.QUOTE:
                    children.append(NodeHelper.__quote_block_to_html_node(b))
                case BlockType.UNORDERED_LIST:
                    children.append(
                        NodeHelper.__unordered_list_block_to_html_node(b))
                case BlockType.ORDERED_LIST:
                    children.append(
                        NodeHelper.__ordered_list_block_to_html_node(b))
                case BlockType.PARAGRAPH:
                    children.append(
                        NodeHelper.__paragraph_block_to_html_node(b))

        parent.children = children
        return parent

    @staticmethod
    def __heading_block_to_html_node(block):
        h_size = 0
        while block[h_size] == "#":
            h_size += 1

        block = (
            block.replace("###### ", "")
            .replace("##### ", "")
            .replace("#### ", "")
            .replace("### ", "")
            .replace("## ", "")
            .replace("# ", "")
        )
        text_nodes = TextNode.text_to_textnodes(block)
        children = [text_node.to_html_node() for text_node in text_nodes]
        return ParentNode(f"h{h_size}", children, None)

    @staticmethod
    def __paragraph_block_to_html_node(block):
        text_nodes = TextNode.text_to_textnodes(block)
        children = [text_node.to_html_node() for text_node in text_nodes]
        return ParentNode("p", children, None)

    @staticmethod
    def __quote_block_to_html_node(block):
        block = block.replace(">", "")
        return LeafNode("blockquote", block, None)

    @staticmethod
    def __code_block_to_html_node(block):
        lines = block.split("\n")
        code_content = "\n".join(lines[1:-1])
        code_content += "\n"
        return ParentNode("pre", [LeafNode("code", code_content, None)], None)

    @staticmethod
    def __unordered_list_block_to_html_node(block):
        lines = block.split("\n")
        bullet_nodes = []
        for line in lines:
            line = line[1:]
            text_nodes = TextNode.text_to_textnodes(line)
            children = [text_node.to_html_node() for text_node in text_nodes]
            bullet_nodes.append(ParentNode("li", children, None))

        return ParentNode("ul", bullet_nodes, None)

    @staticmethod
    def __ordered_list_block_to_html_node(block):
        lines = block.split("\n")
        bullet_nodes = []
        for line in lines:
            idx = line.find(" ") + 1
            line = line[idx:]
            text_nodes = TextNode.text_to_textnodes(line)
            children = [text_node.to_html_node() for text_node in text_nodes]
            bullet_nodes.append(ParentNode("li", children, None))

        return ParentNode("ol", bullet_nodes, None)
