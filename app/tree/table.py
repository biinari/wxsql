"""
Table item in Schema tree.
"""

from item import Item, Container
from column import Column
from index import Index

class Table(Item):
    """ Table item in Schema tree. """

    def expand(self):
        """ Expand table item with containers. """
        columns = self.tree.AppendItem(self.item, 'Columns')
        self.tree.SetItemHasChildren(columns)
        self.tree.SetPyData(columns, ColumnsContainer(self.tree, columns,
            'Columns'))
        indexes = self.tree.AppendItem(self.item, 'Indexes')
        self.tree.SetItemHasChildren(indexes)
        self.tree.SetPyData(indexes, IndexesContainer(self.tree, indexes,
            'Indexes'))

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

class IndexesContainer(Container):
    """ Indexes container item in Schema tree. """

    def expand(self):
        """ Expand table indexes. """
        table = self.tree.GetItemParent(self.item)
        database = self.tree.GetItemParent(self.tree.GetItemParent(table))
        table_name = self.tree.GetItemText(table)
        database_name = self.tree.GetItemText(database)
        for index_name in self._db.get_indexes(database_name, table_name):
            index = self.tree.AppendItem(self.item, index_name)
            self.tree.SetPyData(index, Index(self.tree, index, index_name))
