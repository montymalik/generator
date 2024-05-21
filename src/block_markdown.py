from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    new_markdown = []
    for mark in markdown_split:
        if mark == "":
            continue
        mark = mark.strip()
        new_markdown.append(mark)
    return new_markdown


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def block_to_block_type(markdown):
    markdown_block = markdown.split("\n")
    if markdown.startswith(">"):
        for mark in markdown_block:
            if not mark.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if (
        len(markdown_block) > 1
        and markdown_block[0].startswith("```")
        and markdown_block[-1].startswith("```")
    ):
        return block_type_code
    if (
        markdown.startswith("# ")
        or markdown.startswith("## ")
        or markdown.startswith("### ")
        or markdown.startswith("#### ")
        or markdown.startswith("##### ")
        or markdown.startswith("###### ")
    ):
        return block_type_heading
    if markdown.startswith("* "):
        for mark in markdown_block:
            if not mark.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    if markdown.startswith("- "):
        for mark in markdown_block:
            if not mark.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    if markdown.startswith("1. "):
        i = 1
        for mark in markdown_block:
            if not mark.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(paragraph):
    lines = paragraph.split("\n")
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(heading):
    level = 0
    for char in heading:
        if char == "#":
            level += 1
        else:
            break
        if level + 1 >= len(heading):
            raise ValueError("Invalid Heading")
    text = heading[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(code):
    if not code.startswith("```") or not code.endswith("```"):
        raise ValueError("Invalid Code")
    text = code[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ordered_list_to_html_node(ordered_list):
    items = ordered_list.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(unordered_list):
    items = unordered_list.split('\n')
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(quote):
    lines = quote.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid Quote")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
