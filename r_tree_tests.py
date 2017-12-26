import unittest

from r_tree import RTree, Entry
from rectangle import Rectangle, Point


class RTreeTests(unittest.TestCase):
    def test_add_without_root_should_add_root(self):
        entry_bounds = Rectangle(Point(10, 10), Point(20, 0))
        entry = Entry(name='Tank', bounds=entry_bounds)
        r_tree = RTree(2, 4)
        r_tree.add(entry)

        self.assertIsNotNone(r_tree.root)
        self.assertIsInstance(r_tree.root, RTree.RTreeNode)
        self.assertEqual(r_tree.root.mbr, Rectangle.containing(entry_bounds))
        self.assertEqual(len(r_tree.root.entries), 1)
        self.assertEqual(r_tree.root.entries[0], entry)


if __name__ == '__main__':
    unittest.main()
