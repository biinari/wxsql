"""
Item in Schema tree.
"""

class Item(object):
    """ Abstract Schema Tree Item. """

    def __init__(self, tree, item, name):
        """ Initialise Schema tree item. """
        self.tree = tree
        self.item = item
        self.name = name
        self._db = tree._db

    def expand(self):
        """ Expand item, creating children. """
        raise NotImplementedError

    def collapse(self):
        """ Collapse item. """
        self.tree.Collapse(self.item)

class Container(Item):
    """ Abstract Schema Tree container item. """

    def collapse(self):
        """ Collapse item and remove children. """
        self.tree.CollapseAndReset(self.item)
        self.tree.SetItemHasChildren(item)
