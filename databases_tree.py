#!/usr/bin/env python

import wx
import db

class DatabasesTree(wx.TreeCtrl):

    __collapsing = False

    """ List of databases """
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)

        self.__db = db.DB()
        
        self.__root = self.AddRoot(self.__db.conn.host)
        self.SetItemHasChildren(self.__root)
        self.SetDatabaseItems()

    def SetDatabaseItems(self):
        for database in self.__db.getDatabases():
            item = self.AppendItem(self.__root, database)
            self.SetItemHasChildren(item)

    def OnExpandItem(self, event):
        for table in self.__db.getTables(self.GetItemText(event.GetItem())):
            self.AppendItem(event.GetItem(), table)

    def OnCollapseItem(self, event):
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

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.__tree, 0, wx.EXPAND)
        self.SetSizer(vbox)

if __name__ == "__main__":
    app = wx.App(False)
    frame = DatabasesFrame(None)
    frame.Show(True)
    app.MainLoop()
