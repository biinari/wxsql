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
from ..db.mysql import DB
from database import Database

class SchemaTree(wx.TreeCtrl):
    """ Tree of database schema structure. """

    __collapsing = False

    def __init__(self, *args, **kwargs):
        """ Construct Schema tree. """
        db = kwargs.pop('db')
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expand_item)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.on_collapse_item)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        if db != None:
            self._db = db
        else:
            self._db = DB()
        
        self.__root = self.AddRoot(self._db.conn.host)
        self.SetItemHasChildren(self.__root)
        self.set_database_items()

    def set_database_items(self):
        """ Populate database names. """
        for database_name in self._db.get_databases():
            item = self.AppendItem(self.__root, database_name)
            self.SetItemHasChildren(item)
            self.SetPyData(item, Database(self, item, database_name))

    def on_expand_item(self, event):
        """ Expand an item, populating its children. """
        self.GetPyData(event.GetItem()).expand()

    def on_collapse_item(self, event):
        """ Collapse an item and reset its children. """
        # self.CollapseAndReset below may cause another
        # wx.EVT_TREE_ITEM_COLLAPSING event to be triggered.
        if self.__collapsing:
            event.Veto()
        else:
            self.__collapsing = True
            item = event.GetItem()
            self.GetPyData(item).expand()
            self.SetItemHasChildren(item)
            self.__collapsing = False

    def on_key(self, event):
        """ Improve on <Left> and <Right> key events. """
        key = event.GetKeyCode()
        item = self.GetSelection()

        if key == wx.WXK_LEFT:
            # If the current item is expanded, collapse it.
            if self.IsExpanded(item):
                self.GetPyData(item).collapse()
                return
            # Inhibit moving up
            if self.GetItemParent(item) == self.GetRootItem():
                return
        elif key == wx.WXK_RIGHT:
            # Inhibit moving down
            if not self.ItemHasChildren(item):
                return
            else:
                self.Expand(item)
                if not self.ItemHasChildren(item):
                    return

        event.Skip()

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
