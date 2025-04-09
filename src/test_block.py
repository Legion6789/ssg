import unittest

from block import Block, BlockType


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """
        blocks = Block.markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_is_heading(self):
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("# Text"))
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("## Text"))
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("### Text"))
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("#### Text"))
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("##### Text"))
        self.assertEqual(BlockType.HEADING,
                         Block.block_to_block_type("###### Text"))

    def test_is_not_heading(self):
        self.assertNotEqual(BlockType.HEADING,
                            Block.block_to_block_type("#Text"))
        self.assertNotEqual(BlockType.HEADING,
                            Block.block_to_block_type("####### Text"))
        self.assertNotEqual(BlockType.HEADING,
                            Block.block_to_block_type("Some Text"))

    def test_is_code(self):
        self.assertEqual(
            BlockType.CODE, Block.block_to_block_type("```some code```"))
        self.assertEqual(
            BlockType.CODE, Block.block_to_block_type("``` some code ```"))
        self.assertEqual(
            BlockType.CODE,
            Block.block_to_block_type("``` some code\nsome other code ```"),
        )

    def test_is_not_code(self):
        self.assertNotEqual(
            BlockType.CODE, Block.block_to_block_type("```some code"))
        self.assertNotEqual(
            BlockType.CODE, Block.block_to_block_type(" some code ```"))
        self.assertNotEqual(
            BlockType.CODE, Block.block_to_block_type(
                "`` some code\nsome other code```")
        )

    def test_is_quote(self):
        self.assertEqual(
            BlockType.QUOTE, Block.block_to_block_type(">some quote"))
        self.assertEqual(
            BlockType.QUOTE, Block.block_to_block_type(
                ">some quote\n>another quote")
        )

    def test_is_not_quote(self):
        self.assertNotEqual(
            BlockType.QUOTE, Block.block_to_block_type("ae>ke"))
        self.assertNotEqual(
            BlockType.QUOTE, Block.block_to_block_type(">ae>ke\nhelo"))

    def test_is_unordered_list(self):
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            Block.block_to_block_type("- item 1\n- item 2\n- item 3"),
        )
        self.assertEqual(BlockType.UNORDERED_LIST,
                         Block.block_to_block_type("- item 1"))

    def test_is_not_unordered_list(self):
        self.assertNotEqual(BlockType.UNORDERED_LIST,
                            Block.block_to_block_type("item 1"))
        self.assertNotEqual(
            BlockType.UNORDERED_LIST, Block.block_to_block_type(
                "- item 1\nitem 2")
        )

    def test_is_ordered_list(self):
        self.assertEqual(BlockType.ORDERED_LIST,
                         Block.block_to_block_type("1. first"))
        self.assertEqual(
            BlockType.ORDERED_LIST,
            Block.block_to_block_type("1. first\n2. second\n3. third"),
        )

    def test_is_not_ordered_list(self):
        self.assertNotEqual(
            BlockType.ORDERED_LIST, Block.block_to_block_type(
                " . first\n2. second")
        )
        self.assertNotEqual(
            BlockType.ORDERED_LIST, Block.block_to_block_type(
                "1. first\n. second")
        )
        self.assertNotEqual(
            BlockType.ORDERED_LIST, Block.block_to_block_type(
                "1. first\n . second")
        )
        self.assertNotEqual(
            BlockType.ORDERED_LIST,
            Block.block_to_block_type("1. first\n4. second\n3. third"),
        )

    def test_is_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH,
                         Block.block_to_block_type("any old text"))
        self.assertEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type(
                "any old text\nmore text")
        )
        self.assertEqual(BlockType.PARAGRAPH,
                         Block.block_to_block_type("#stuff"))
        self.assertEqual(BlockType.PARAGRAPH,
                         Block.block_to_block_type("```stuff"))
        self.assertEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type(
                "stuff\n>more stuff")
        )
        self.assertEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type(
                "stuff\n- more stuff")
        )
        self.assertEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type(
                "1.stuff\n2. more stuff")
        )

    def test_is_not_paragraph(self):
        self.assertNotEqual(BlockType.PARAGRAPH,
                            Block.block_to_block_type("# Header"))
        self.assertNotEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type("``` Code ```")
        )
        self.assertNotEqual(BlockType.PARAGRAPH,
                            Block.block_to_block_type(">Quote"))
        self.assertNotEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type("- Unordered Item")
        )
        self.assertNotEqual(
            BlockType.PARAGRAPH, Block.block_to_block_type("1. First Item")
        )


if __name__ == "__main__":
    unittest.main()
