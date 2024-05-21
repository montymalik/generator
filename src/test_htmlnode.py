import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

import unittest
from unittest.mock import MagicMock

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_props_none(self):
        node = HTMLNode()
        node.props = None
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_props_empty(self):
        node = HTMLNode()
        node.props = {}
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_key_value_pair(self):
        node = HTMLNode()
        node.props = {"class": "my-class"}
        self.assertEqual(node.props_to_html(), " class=\"my-class\"")

    def test_props_to_html_multiple_key_value_pairs(self):
        node = HTMLNode()
        node.props = {"class": "my-class", "id": "my-id"}
        self.assertIn(" class=\"my-class\"", node.props_to_html())
        self.assertIn(" id=\"my-id\"", node.props_to_html())
        self.assertEqual(node.props_to_html(),
                         " class=\"my-class\" id=\"my-id\"")


class TestLeafNode(unittest.TestCase):
    def test_to_html_raise_value_error(self):
        node = LeafNode(None, None, {"class": "my-class"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_tag_none(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_to_html_multiple_props(self):
        node = LeafNode("h1", "Heading", {"class": "my-class", "id": "my-id"})
        self.assertEqual(
            node.to_html(), "<h1 class=\"my-class\" id=\"my-id\">Heading</h1>")

    def test_to_html_one_prop(self):
        node = LeafNode("h1", "Heading", {"class": "my-class"})
        self.assertEqual(node.to_html(), "<h1 class=\"my-class\">Heading</h1>")

    def test_to_html_no_props(self):
        node = LeafNode("h1", "Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")


class TestParentNodeToHtml(unittest.TestCase):

    def test_to_html_raise_value_error_tag_none(self):
        node = ParentNode(None, [MagicMock()])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raise_value_error_children_none(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_one_child(self):
        child = MagicMock()
        child.to_html.return_value = "<p>Child</p>"

        node = ParentNode("div", [child])
        expected_output = "<div><p>Child</p></div>"

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_multiple_children(self):
        child1 = MagicMock()
        child1.to_html.return_value = "<p>Child1</p>"
        child2 = MagicMock()
        child2.to_html.return_value = "<p>Child2</p>"

        node = ParentNode("div", [child1, child2])
        expected_output = "<div><p>Child1</p><p>Child2</p></div>"

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_one_prop(self):
        child = MagicMock()
        child.to_html.return_value = "<p>Child</p>"

        node = ParentNode("div", [child], {"class": "my-class"})
        expected_output = "<div class=\"my-class\"><p>Child</p></div>"

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_multiple_props(self):
        child = MagicMock()
        child.to_html.return_value = "<p>Child</p>"

        node = ParentNode("div", [child], {"class": "my-class", "id": "my-id"})
        expected_output = "<div class=\"my-class\" id=\"my-id\"><p>Child</p></div>"

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_no_props(self):
        child = MagicMock()
        child.to_html.return_value = "<p>Child</p>"

        node = ParentNode("div", [child])
        expected_output = "<div><p>Child</p></div>"

        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == '__main__':
    unittest.main()