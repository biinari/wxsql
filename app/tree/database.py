"""
Database item in Schema tree.
"""

from item import Item, Container
from table import Table

class Database(Item):
    """ Database item in Schema tree. """

    def expand(self):
        """ Expand database item with containers. """
        for container_name in ['Tables']:
            container = self.tree.AppendItem(self.item, container_name)
            self.tree.SetItemHasChildren(container)
            self.tree.SetPyData(container, TablesContainer(self.tree, container,
                container_name))

class TablesContainer(Container):
    """ Tables container item in Schema tree. """

    def expand(self):
        """ Expand Tables container. """
        database_name = self.tree.GetItemText(self.tree.GetItemParent(self.item))
        for table_name in self._db.get_tables(database_name):
            table = self.tree.AppendItem(self.item, table_name)
            self.tree.SetItemHasChildren(table)
            self.tree.SetPyData(table, Table(self.tree, table, table_name))
