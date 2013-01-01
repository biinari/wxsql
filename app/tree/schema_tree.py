#!/usr/bin/env python
"""
Tree of database structure.

Tree structure will contain the following nested levels of items:

    Database:
        Table:
            Columns:
            Indexes:
"""

import wx
from app.db.mysql import DB

class SchemaTree(wx.TreeCtrl):
    """ Tree of database schema structure. """

    __collapsing = False

    def __init__(self, *args, **kwargs):
        """ Construct Schema tree. """
        db = kwargs.pop('db')
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expand_item)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.on_collapse_item)

        if db != None:
            self.__db = db
        else:
            self.__db = DB()
        
        self.__root = self.AddRoot(self.__db.conn.host)
        self.SetItemHasChildren(self.__root)
        self.set_database_items()

    def set_database_items(self):
        """ Populate database names. """
        for database in self.__db.get_databases():
            item = self.AppendItem(self.__root, database)
            self.SetItemHasChildren(item)
            for container_name in ['Tables']:
                container = self.AppendItem(item, container_name)
                self.SetItemHasChildren(container)

    def is_database(self, item):
        """ Return True if item is a database. """
        return self.GetItemParent(item) == self.__root

    def is_tables_container(self, item):
        """ Return True if item is a tables container. """
        return self.GetItemText(item) == 'Tables' and \
                self.is_database(self.GetItemParent(item))

    def is_table(self, item):
        """ Return True if item is a table. """
        return self.is_tables_container(self.GetItemParent(item))

    def is_columns_container(self, item):
        """ Return True if item is a columns container. """
        return self.GetItemText(item) == 'Columns' and \
                self.is_table(self.GetItemParent(item))

    def expand_tables(self, item):
        database_name = self.GetItemText(self.GetItemParent(item))
        for table_name in self.__db.get_tables(database_name):
            table = self.AppendItem(item, table_name)
            self.SetItemHasChildren(table)
            for container_name in ['Columns', 'Indexes']:
                container = self.AppendItem(table, container_name)
                self.SetItemHasChildren(container)

    def expand_columns(self, item):
        table = self.GetItemParent(item)
        database = self.GetItemParent(self.GetItemParent(table))
        table_name = self.GetItemText(table)
        database_name = self.GetItemText(database)
        for column_name in self.__db.get_columns(database_name, table_name):
            self.AppendItem(item, column_name)

    def on_expand_item(self, event):
        """ Expand an item, populating its children. """
        item = event.GetItem()
        if self.is_tables_container(item):
            self.expand_tables(item)
        elif self.is_columns_container(item):
            self.expand_columns(item)

    def on_collapse_item(self, event):
        """ Collapse an item and reset its children. """
        # self.CollapseAndReset below may cause another
        # wx.EVT_TREE_ITEM_COLLAPSING event to be triggered.
        if self.__collapsing:
            event.Veto()
        else:
            self.__collapsing = True
            item = event.GetItem()
            self.CollapseAndReset(item)
            self.SetItemHasChildren(item)
            self.__collapsing = False

class SchemaTreeFrame(wx.Frame):
    """ Test frame for database structure tree. """

    def __init__(self, *args, **kwargs):
        """ Create test frame for database structure tree. """
        wx.Frame.__init__(self, *args, **kwargs)
        self.__tree = SchemaTree(self, size=(200, 400),
                                    style=wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE)
        self.__display = wx.StaticText(self)

        self.__tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.__tree, 1, wx.EXPAND)
        hbox.Add(self.__display, 1, wx.EXPAND | wx.TOP | wx.LEFT, 10)
        self.SetSizer(hbox)
        self.Centre()

    def on_sel_changed(self, event):
        """ Display selected item in static text object. """
        self.__display.SetLabel(self.__tree.GetItemText(event.GetItem()))

def main():
    app = wx.App(False)
    frame = SchemaTreeFrame(None, size=(600, 450))
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()
