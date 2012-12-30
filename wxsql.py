#!/usr/bin/env python
import wx

from .app.db.mysql import DB
from .databases_tree import DatabasesTree
from .query_editor import QueryEditorPanel

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
        horiz_split = wx.SplitterWindow(self, style=wx.SP_3D)
        horiz_split.SetMinimumPaneSize(20)
        left_vert_split = wx.SplitterWindow(horiz_split, style=wx.SP_3D)
        left_vert_split.SetMinimumPaneSize(20)
        self.databases_tree = DatabasesTree(left_vert_split, db=self._db,
                size=(200, 300), style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
        self.query_editor = QueryEditorPanel(horiz_split)
        self.display = wx.StaticText(left_vert_split,
                label="Select a database above")

        self.databases_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnDBSelChanged)

        left_vert_split.SplitHorizontally(self.databases_tree, self.display)
        horiz_split.SplitVertically(left_vert_split, self.query_editor)

    """ Setup menu bar. """
    def CreateMenu(self):
        file_menu = wx.Menu()
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Quit")

        help_menu = wx.Menu()
        menu_about = help_menu.Append(wx.ID_ABOUT, "&About", "About wxSQL")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)

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
        text = self.databases_tree.GetItemText(item)
        if self.databases_tree.IsDatabase(item):
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
