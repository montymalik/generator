import unittest

from block_markdown import block_to_block_type, markdown_to_blocks, block_type_paragraph, block_type_heading, block_type_code, block_type_quote, block_type_unordered_list, block_type_ordered_list, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):

    def test_empty_input(self):
        result = markdown_to_blocks("")
        self.assertEqual(result, [])

    def test_multiple_blocks(self):
        input_str = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(input_str)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_whitespace_blocks(self):
        input_str = "   Block 1   \n\n   Block 2   \n\n   Block 3   "
        result = markdown_to_blocks(input_str)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_heading_block(self):
        result = block_to_block_type("# Heading")
        self.assertEqual(result, block_type_heading)

    def test_code_block(self):
        result = block_to_block_type("```\nCode\n```")
        self.assertEqual(result, block_type_code)

    def test_quote_block(self):
        result = block_to_block_type("> Quote")
        self.assertEqual(result, block_type_quote)

    def test_unordered_list_block(self):
        result = block_to_block_type("* Item 1")
        self.assertEqual(result, block_type_unordered_list)

    def test_ordered_list_block(self):
        result = block_to_block_type("1. Item 1")
        self.assertEqual(result, block_type_ordered_list)

    def test_paragraph_block(self):
        result = block_to_block_type("This is a regular paragraph")
        self.assertEqual(result, block_type_paragraph)

    def test_empty_block(self):
        result = block_to_block_type("")
        self.assertEqual(result, block_type_paragraph)

    def test_mixed_list_block(self):
        result = block_to_block_type("* Item 1\n- Item 2")
        self.assertEqual(result, block_type_paragraph)

    def test_invalid_list_format(self):
        result = block_to_block_type("* Item 1\n* Item 2\n3. Item 3")
        self.assertEqual(result, block_type_paragraph)

    def test_invalid_heading_format(self):
        result = block_to_block_type("#Heading")
        self.assertEqual(result, block_type_paragraph)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == '__main__':
    unittest.main()