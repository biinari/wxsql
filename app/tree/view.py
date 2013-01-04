"""
View item in Schema tree.
"""

from item import Item, Container
from table import ColumnsContainer, IndexesContainer

class View(Item):
    """ View item in Schema tree. """
    
    def expand(self):
        """ Expand view item with containers. """
        columns = self.tree.AppendItem(self.item, 'Columns')
        self.tree.SetItemHasChildren(columns)
        self.tree.SetPyData(columns, ColumnsContainer(self.tree, columns,
            'Columns'))
        indexes = self.tree.AppendItem(self.item, 'Indexes')
        self.tree.SetItemHasChildren(indexes)
        self.tree.SetPyData(indexes, IndexesContainer(self.tree, indexes,
            'Indexes'))
