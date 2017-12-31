from rectangle import Rectangle, Point, RectangleResizer


class Entry:
    """
    An entry in the R-Tree
    """
    def __init__(self, name: str, bounds: Rectangle):
        self.name = name
        self.mbr = bounds

    def __eq__(self, other):
        return self.name == other.name and self.mbr == other.mbr


class RTree:

    class RTreeNode:
        """
        A node in the R-Tree
        """
        def __init__(self, min_order: int, max_order: int, mbr: Rectangle=Rectangle(Point(0, 1), Point(1, 0))):
            self.mbr: Rectangle = mbr
            self.minimum_order = min_order
            self.maximum_order = max_order
            self.children = []
            self.entries = []

        def add(self, object: Entry):
            if len(self.children) == 0:
                # This node is a leaf, add the entry
                if len(self.entries) == self.maximum_order:
                    # Need to split
                    node_a, node_b = self.split_leaf()
                    # TODO: Expand parents' MBR and re-assign
                self.entries.append(object)
                # TODO: Handle full entries case
                return
            pass

        def split_leaf(self):
            """
            Splits the given RTreeNode into 2 separate Nodes
            """
            if len(self.children) > 0:
                raise NotImplementedError('[DEBUG] Unexpected behavior')
            # 1. Find the two most far-apart objects
            max_distance = -1
            max_obj_a, max_obj_b = None, None
            for idx, entry in enumerate(self.entries):
                for idx_2 in range(len(self.entries)):
                    if idx == idx_2:
                        continue
                    other_entry = self.entries[idx_2]

                    dist = entry.mbr.distance_between(other_entry.mbr)
                    if dist > max_distance:
                        max_obj_a = entry
                        max_obj_b = other_entry

            # 2. Create two new nodes to accommodate the new objects
            node_a = RTreeNode(min_order=self.minimum_order, max_order=self.maximum_order,
                               mbr=Rectangle.containing(max_obj_a.mbr))
            node_a.add(max_obj_a)
            node_b = RTreeNode(min_order=self.minimum_order, max_order=self.maximum_order,
                               mbr=Rectangle.containing(max_obj_b.mbr))
            node_b.add(max_obj_b)

            # 3. Move rest of entries to appropriate nodes
            rest_entries = [entry for entry in self.entries if entry != max_obj_a and entry != max_obj_b]
            for idx, entry in enumerate(rest_entries):
                rest_entry_count = len(rest_entries) - idx
                needed_a_entries = node_a.minimum_order - len(node_a.entries)
                needed_b_entries = node_b.minimum_order - len(node_b.entries)
                if rest_entry_count == needed_a_entries:
                    node_a.add(entry)  # All the rest should go to A
                elif rest_entry_count == needed_b_entries:
                    node_b.add(entry)  # All the rest should go to B
                else:
                    # Put it in the one whose MBR requires least expansion
                    # TODO: Handle case where both bound entry
                    if node_a.mbr.is_bounding(entry.mbr):
                        node_a.add(entry)
                    elif node_b.mbr.is_bounding(entry.mbr):
                        node_b.add(entry)
                    else:
                        orig_a_area = node_a.mbr.area
                        orig_b_area = node_b.mbr.area
                        expanded_a_area = RectangleResizer.rectangle_expanded_to(node_a.mbr, entry.mbr).area
                        expanded_b_area = RectangleResizer.rectangle_expanded_to(node_b.mbr, entry.mbr).area
                        if expanded_a_area >= expanded_b_area:
                            node_b.add(entry)
                        else:
                            node_a.add(entry)

            return node_a, node_b

    def __init__(self, min_order: int, max_order: int):
        self.root: self.RTreeNode = None
        self.minimum_order = min_order
        self.maximum_order = max_order

    def add(self, object: Entry):
        if self.root is None:
            self.root: self.RTreeNode = self.RTreeNode(mbr=Rectangle.containing(object.mbr),
                                                       min_order=self.minimum_order, max_order=self.maximum_order)
        self.root.add(object)
