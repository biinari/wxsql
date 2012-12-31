#!/usr/bin/env python

import wx
from .app.db.mysql import DB

class DatabasesTree(wx.TreeCtrl):

    __collapsing = False

    """ List of databases """
    def __init__(self, *args, **kwargs):
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
        for database in self.__db.getDatabases():
            item = self.AppendItem(self.__root, database)
            self.SetItemHasChildren(item)

    def is_database(self, item):
        return self.GetItemParent(item) == self.__root

    def on_expand_item(self, event):
        for table in self.__db.getTables(self.GetItemText(event.GetItem())):
            self.AppendItem(event.GetItem(), table)

    def on_collapse_item(self, event):
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
    def __init__(self, *args, **kwargs):
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
        self.__display.SetLabel(self.__tree.GetItemText(event.GetItem()))

if __name__ == "__main__":
    app = wx.App(False)
    frame = DatabasesFrame(None, size=(600, 450))
    frame.Show(True)
    app.MainLoop()
