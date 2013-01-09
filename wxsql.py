#!/usr/bin/env python
""" wxSQL, a front end for MySQL written in wxPython """

import wx

from app.db.mysql import DB
from app.tree.schema_tree import SchemaTree
from app.editor.editor import QueryEditorPanel
from app.result.table import ResultTablePanel

class MainWindow(wx.Frame):
    """ Main Window frame for wxSQL """

    def __init__(self, parent, title):
        """ Main Window Frame for wxSQL """
        wx.Frame.__init__(self, parent, title=title)
        self.SetClientSize((600, 450))
        self._db = DB()
        self.create_panels()
        self.create_menu()
        self.Show(True)

    def create_panels(self):
        """ Layout user resizable panels """
        horiz_split = wx.SplitterWindow(self, style=wx.SP_3D)
        left_split = wx.SplitterWindow(horiz_split, style=wx.SP_3D)
        right_split = wx.SplitterWindow(horiz_split, style=wx.SP_3D)
        self.schema_tree = SchemaTree(left_split, db=self._db,
                style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
        self.display = wx.StaticText(left_split,
                label="Select a database above")
        self.query_editor = QueryEditorPanel(right_split)
        self.results = ResultTablePanel(right_split)

        self.schema_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_db_sel_change)

        left_split.SplitHorizontally(self.schema_tree, self.display, -150)
        right_split.SplitHorizontally(self.query_editor, self.results, -150)
        horiz_split.SplitVertically(left_split, right_split)
        horiz_split.SetMinimumPaneSize(100)
        left_split.SetMinimumPaneSize(100)
        right_split.SetMinimumPaneSize(100)

    def create_menu(self):
        """ Setup menu bar. """
        file_menu = wx.Menu()
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Quit")

        help_menu = wx.Menu()
        menu_about = help_menu.Append(wx.ID_ABOUT, "&About", "About wxSQL")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)

    def on_about(self, event):
        """ Show About dialog """
        about = wx.MessageDialog(
            self,
            "Work with MySQL databases",
            "About wxSQL",
            wx.OK)
        about.ShowModal()
        about.Destroy()

    def on_db_sel_change(self, event):
        """ Database tree selection changed """
        item = event.GetItem()
        text = self.schema_tree.GetItemText(item)
        item_type = self.schema_tree.GetPyData(item).__class__.__name__
        self.display.SetLabel("Type: %s" % item_type)

        if item_type == 'Database':
            self._db.select_database(text)
            self.display.SetLabel("db: %s" % text)
        elif item_type == 'Table':
            self.display.SetLabel("table: %s" % text)
        elif item_type == 'View':
            self.display.SetLabel("view: %s" % text)
        elif item_type == 'Column':
            self.display.SetLabel("column: %s" % text)
        elif item_type == 'Index':
            self.display.SetLabel("index: %s" % text)

    def on_exit(self, event):
        """ Exit application """
        self.Close(True)

def main():
    app = wx.App(False)
    frame = MainWindow(None, "wxSQL")
    app.MainLoop()

if __name__ == '__main__':
    main()
