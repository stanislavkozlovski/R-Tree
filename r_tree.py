from rectangle import Rectangle, Point


class Entry:
    """
    An entry in the R-Tree
    """
    def __init__(self, name: str, bounds: Rectangle):
        self.name = name
        self.bounds = bounds


class RTree:

    class RTreeNode:
        """
        A node in the R-Tree
        """
        def __init__(self, mbr: Rectangle=Rectangle(Point(0, 0), Point(0, 0))):
            self.mbr = mbr
            self.children = []
            self.entries = []

        def add(self, object: Entry):
            if len(self.children) == 0:
                # This node is a leaf, add the entry
                self.entries.append(object)
                # TODO: Handle full entries case
                return
            pass

    def __init__(self, min_order: int, max_order: int):
        self.root: self.RTreeNode = None
        self.minimum_order = min_order
        self.maximum_order = max_order

    def add(self, object: Entry):
        if self.root is None:
            self.root: self.RTreeNode = self.RTreeNode(mbr=object.bounds)
            return
        self.root.add(object)
