from rectangle import Rectangle, Point, RectangleResizer


class Entry:
    """
    An entry in the R-Tree
    """
    def __init__(self, name: str, bounds: Rectangle):
        self.name = name
        self.mbr: Rectangle = bounds

    def __eq__(self, other):
        return self.name == other.name and self.mbr == other.mbr

    def __hash__(self):
        return hash(f'{self.name}{hash(self.mbr)}')


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
            self.entries: [Entry] = []

        def add(self, object: Entry):
            if len(self.children) == 0:
                # This node is a leaf, add the entry
                self.entries.append(object)

                if not self.mbr.is_bounding(object.mbr):
                    self.mbr.expand_to(object.mbr)

                if len(self.entries) == self.maximum_order:
                    # Need to split
                    node_a, node_b = self.split_leaf()
                    self.children.extend([node_a, node_b])
                return
            pass

        def split_leaf(self):
            """
            Splits the given RTreeNode into 2 separate Nodes
            Then moves its entries into one of the two nodes
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
                        max_distance = dist
                        max_obj_a = entry
                        max_obj_b = other_entry

            # 2. Create two new nodes to accommodate the new objects
            node_a = self.__class__(min_order=self.minimum_order, max_order=self.maximum_order,
                                    mbr=Rectangle.containing(max_obj_a.mbr))
            node_a.add(max_obj_a)
            node_b = self.__class__(min_order=self.minimum_order, max_order=self.maximum_order,
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
                    node: 'RTreeNode' = self.find_min_expansion_node([node_a, node_b], entry)
                    node.add(entry)

            # 4. Expand node's MBR to fir their biggest
            for node in [node_a, node_b]:
                for entry in node.entries:
                    entry: Entry
                    if not node.mbr.is_bounding(entry.mbr):
                        node.mbr.expand_to(entry.mbr)

            return node_a, node_b

        @staticmethod
        def find_min_expansion_node(rt_nodes: ['RTreeNode'], entry: Entry) -> 'RTreeNode':
            """
            Given N RTreeNodes and one Entry,
                find the RTreeNode which requires the least expansion to accommodate the Entry
            """
            expansions = []
            for node in rt_nodes:
                if node.mbr.is_bounding(entry.mbr):
                    expanded = 0
                else:
                    expanded = RectangleResizer.rectangle_expanded_to(node.mbr, entry.mbr).area - node.mbr.area
                expansions.append({'node': node, 'expanded': expanded})

            return min(expansions, key=lambda x: x['expanded'])['node']

    def __init__(self, min_order: int, max_order: int):
        self.root: self.RTreeNode = None
        self.minimum_order = min_order
        self.maximum_order = max_order

    def add(self, object: Entry):
        if self.root is None:
            self.root: self.RTreeNode = self.RTreeNode(mbr=Rectangle.containing(object.mbr),
                                                       min_order=self.minimum_order, max_order=self.maximum_order)
        self.root.add(object)
