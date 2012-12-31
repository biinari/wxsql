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

class DatabasesTree(wx.TreeCtrl):
    """ Tree of database structure. """

    __collapsing = False

    def __init__(self, *args, **kwargs):
        """ Construct Database structure tree. """
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

    def is_database(self, item):
        """ Return True if selected item is at database level. """
        return self.GetItemParent(item) == self.__root

    def on_expand_item(self, event):
        """ Expand an item, populating its children. """
        for table in self.__db.get_tables(self.GetItemText(event.GetItem())):
            self.AppendItem(event.GetItem(), table)

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

class DatabasesFrame(wx.Frame):
    """ Test frame for database structure tree. """

    def __init__(self, *args, **kwargs):
        """ Create test frame for database structure tree. """
        wx.Frame.__init__(self, *args, **kwargs)
        self.__tree = DatabasesTree(self, size=(200, 400),
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

if __name__ == "__main__":
    app = wx.App(False)
    frame = DatabasesFrame(None, size=(600, 450))
    frame.Show(True)
    app.MainLoop()
