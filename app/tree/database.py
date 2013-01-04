"""
Database item in Schema tree.
"""

from item import Item, Container
from table import Table
from view import View

class Database(Item):
    """ Database item in Schema tree. """

    def expand(self):
        """ Expand database item with containers. """
        tables = self.tree.AppendItem(self.item, 'Tables')
        self.tree.SetItemHasChildren(tables)
        self.tree.SetPyData(tables, TablesContainer(self.tree, tables, 'Tables'))
        views = self.tree.AppendItem(self.item, 'Views')
        self.tree.SetItemHasChildren(views)
        self.tree.SetPyData(views, ViewsContainer(self.tree, views, 'Views'))

class TablesContainer(Container):
    """ Tables container item in Schema tree. """

    def expand(self):
        """ Expand Tables container. """
        database_name = self.tree.GetItemText(self.tree.GetItemParent(self.item))
        for table_name in self._db.get_tables(database_name):
            table = self.tree.AppendItem(self.item, table_name)
            self.tree.SetItemHasChildren(table)
            self.tree.SetPyData(table, Table(self.tree, table, table_name))

class ViewsContainer(Container):
    """ Views container item in Schema tree. """

    def expand(self):
        """ Expand Views container. """
        database_name = self.tree.GetItemText(self.tree.GetItemParent(self.item))
        for view_name in self._db.get_views(database_name):
            view = self.tree.AppendItem(self.item, view_name)
            self.tree.SetItemHasChildren(view)
            self.tree.SetPyData(view, View(self.tree, view, view_name))
