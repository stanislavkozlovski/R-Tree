from rectangle import Rectangle, Point


class Entry:
    """
    An entry in the R-Tree
    """
    def __init__(self, name: str, bounds: Rectangle):
        self.name = name
        self.mbr = bounds


class RTree:

    class RTreeNode:
        """
        A node in the R-Tree
        """
        def __init__(self, max_order: int, mbr: Rectangle=Rectangle(Point(0, 1), Point(1, 0))):
            self.mbr = mbr
            self.maximum_order = max_order
            self.children = []
            self.entries = []

        def add(self, object: Entry):
            if len(self.children) == 0:
                # This node is a leaf, add the entry
                if len(self.entries) == self.maximum_order:
                    # Need to split
                    pass
                self.entries.append(object)
                # TODO: Handle full entries case
                return
            pass

        def split(self):
            """
            Splits the given RTreeNode into 2 separate Nodes
            :return:
            """
            pass

    def __init__(self, min_order: int, max_order: int):
        self.root: self.RTreeNode = None
        self.minimum_order = min_order
        self.maximum_order = max_order

    def add(self, object: Entry):
        if self.root is None:
            self.root: self.RTreeNode = self.RTreeNode(mbr=Rectangle.containing(object.mbr), max_order=self.maximum_order)
        self.root.add(object)
