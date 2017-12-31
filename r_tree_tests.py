import unittest

from r_tree import RTree, Entry
from rectangle import Rectangle, Point

RTreeNode = RTree.RTreeNode
POINT_OFFSET = Point.MOVE_DISTANCE


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

    def test_add_bigger_mbr_entry_expands_root(self):
        r_tree = RTree(2, 4)
        s_entry = Entry('SMALL_MAN', bounds=Rectangle(Point(52, 43), Point(68, 22)))
        expected_root_mbr = Rectangle(Point(52 - POINT_OFFSET, 43 + POINT_OFFSET), Point(68 + POINT_OFFSET, 22 - POINT_OFFSET))
        r_tree.add(s_entry)
        self.assertEqual(r_tree.root.mbr, expected_root_mbr)

        # Add a bigger entry
        expected_root_mbr = Rectangle(Point(20 - POINT_OFFSET, 45 + POINT_OFFSET), Point(70 + POINT_OFFSET, 20 - POINT_OFFSET))
        b_entry = Entry('BIG_MAN', Rectangle(Point(20, 45), Point(70, 20)))
        r_tree.add(b_entry)

        self.assertEqual(r_tree.root.mbr, expected_root_mbr)
        self.assertCountEqual(r_tree.root.entries, [b_entry, s_entry])


    """
    The split_leaf function should split a leaf full of entries into two separate nodes.
    It should pick the two furthest apart entries and make their MBRs into nodes.
        Then, from the left-over entries, it should choose to insert them into the node which requires least expansion
    """
    def test_split(self):
        """
        -----------------------------------------------------------------------------------------------------
        |                                                      |------------------------------------------| |
        |                                                      |                                          | |
        |                                         ______       |                                          | |
        |     ______________                      |     |      |                                          | |
        |    |             |                      |     |      |                                          | |
        |    |     A       |                      |     |      |                                          | |
        |    |             |                      |     |      |                                          | |
        |    |     ________|________              |     |      |                                          | |
        |    |     |       |       |              |  C  |      |                  D                       | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |B      |              |     |      |                                          | |
        |    --------------        |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          -----------------              |     |      |                                          | |
        |                                         -------      |                                          | |
        |                                                      |                                          | |
        |                                                      |__________________________________________| |
        |                                                                                                   |
        _____________________________________________________________________________________________________

        Here, A and D should be chosen as the basis for the two new nodes.
            B should go to the A node and C should go to the D node, as that would require the least expansion from both sides

        -----------------------------------------------------------------------------------------------------
        |                                        _____________________________Node B________________________|
        |                                        |             |------------------------------------------|||
        |                                        |             |                                          |||
        |  ______Node A______________            |______       |                                          |||
        |  |  ______________        |            ||     |      |                                          |||
        |  | |             |        |            ||     |      |                                          |||
        |  | |     A       |        |            ||     |      |                                          |||
        |  | |             |        |            ||     |      |                                          |||
        |  | |     ________|________|            ||     |      |                                          |||
        |  | |     |       |       ||            ||  C  |      |                  D                       |||
        |  | |     |       |       ||            ||     |      |                                          |||
        |  | |     |       |       ||            ||     |      |                                          |||
        |  | |     |       |B      ||            ||     |      |                                          |||
        |  | --------------        ||            ||     |      |                                          |||
        |  |       |               ||            ||     |      |                                          |||
        |  |       |               ||            ||     |      |                                          |||
        |  |       -----------------|            ||     |      |                                          |||
        |  |------------------------|            |-------      |                                          |||
        |                                        |             |                                          |||
        |                                        |             |__________________________________________|||
        |                                         --------------------------------------------------------- |
        ____________________________________________________________________________________________________|

       Both nodes should be 1 point bigger than the nodes
        """
        root = RTreeNode(2, 4, Rectangle(Point(20, 45), Point(70, 20)))
        entry_a = Entry('A', bounds=Rectangle(Point(22, 40), Point(30, 30)))
        entry_b = Entry('B', bounds=Rectangle(Point(25, 35), Point(40, 25)))
        entry_c = Entry('C', bounds=Rectangle(Point(44, 40), Point(47, 25)))
        entry_d = Entry('D', bounds=Rectangle(Point(52, 43), Point(68, 22)))
        root.entries = [entry_a, entry_b, entry_c, entry_d]

        expected_node_a_mbr = Rectangle(Point(22 - POINT_OFFSET, 40 + POINT_OFFSET),
                                        Point(40 + POINT_OFFSET, 25 - POINT_OFFSET))
        expected_node_b_mbr = Rectangle(Point(44 - POINT_OFFSET, 43 + POINT_OFFSET),
                                        Point(68 + POINT_OFFSET, 22 - POINT_OFFSET))

        node_a, node_b = root.split_leaf()

        self.assertEqual(node_a.mbr, expected_node_a_mbr)
        self.assertEqual(node_b.mbr, expected_node_b_mbr)
        self.assertCountEqual(node_a.entries, [entry_a, entry_b])
        self.assertCountEqual(node_b.entries, [entry_c, entry_d])
        self.assertEqual(node_a.children, [])
        self.assertEqual(node_b.children, [])


if __name__ == '__main__':
    unittest.main()
