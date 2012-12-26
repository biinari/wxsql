#!/usr/bin/env python
import wx

from app.db.mysql import DB
from databases_tree import DatabasesTree
from query_editor import QueryEditorPanel

class MainWindow(wx.Frame):

    """ Main Window Frame for wxSQL """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.SetClientSize((600, 450))
        self._db = DB()
        self.CreateFrames()
        self.CreateMenu()
        self.Show(True)

    def CreateFrames(self):
        horizSplitter = wx.SplitterWindow(self, style=wx.SP_3D)
        horizSplitter.SetMinimumPaneSize(20)
        leftVSplitter = wx.SplitterWindow(horizSplitter, style=wx.SP_3D)
        leftVSplitter.SetMinimumPaneSize(20)
        self.databasesTree = DatabasesTree(leftVSplitter, db=self._db, size=(200, 300),
                style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
        self.queryEditor = QueryEditorPanel(horizSplitter)
        self.display = wx.StaticText(leftVSplitter, label="Select a database above")

        self.databasesTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnDBSelChanged)

        leftVSplitter.SplitHorizontally(self.databasesTree, self.display)
        horizSplitter.SplitVertically(leftVSplitter, self.queryEditor)

    """ Setup menu bar. """
    def CreateMenu(self):
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Quit")

        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "About wxSQL")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

    def OnAbout(self, event):
        about = wx.MessageDialog(
            self,
            "Work with MySQL databases",
            "About wxSQL",
            wx.OK)
        about.ShowModal()
        about.Destroy()

    def OnDBSelChanged(self, event):
        item = event.GetItem()
        text = self.databasesTree.GetItemText(item)
        if self.databasesTree.IsDatabase(item):
            self._db.selectDatabase(text)
            self.display.SetLabel("db: %s" % text)
        else:
            self.display.SetLabel("table: %s" % text)

    def OnExit(self, event):
        self.Close(True)

def main():
    app = wx.App(False)
    frame = MainWindow(None, "wxSQL")
    app.MainLoop()

if __name__ == '__main__':
    main()
