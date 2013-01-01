"""
Table item in Schema tree.
"""

from item import Item, Container
from column import Column

class Table(Item):
    """ Table item in Schema tree. """

    def expand(self):
        """ Expand table item with containers. """
        for container_name in ['Columns', 'Indexes']:
            container = self.tree.AppendItem(self.item, container_name)
            self.tree.SetItemHasChildren(container)
            self.tree.SetPyData(container, ColumnsContainer(self.tree,
                container, container_name))

class ColumnsContainer(Container):
    """ Columns container item in Schema tree. """

    def expand(self):
        """ Expand table columns. """
        table = self.tree.GetItemParent(self.item)
        database = self.tree.GetItemParent(self.tree.GetItemParent(table))
        table_name = self.tree.GetItemText(table)
        database_name = self.tree.GetItemText(database)
        for column_name in self._db.get_columns(database_name, table_name):
            column = self.tree.AppendItem(self.item, column_name)
            self.tree.SetPyData(column, Column(self.tree, column, column_name))
