#!/usr/bin/env python
import wx

from databases_tree import DatabasesTree

class MainWindow(wx.Frame):

    """ Main Window Frame for wxSQL """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(610, 550))
        self.CreateFrames()
        self.CreateMenu()
        self.Show(True)

    def CreateFrames(self):
        grid = wx.GridBagSizer(5, 5)
        self.databasesTree = DatabasesTree(self, size=(200, 400),
                style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
        grid.Add(self.databasesTree, (0, 0))
        self.SetSizer(grid)
        self.Centre()

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

    def OnExit(self, event):
        self.Close(True)

def main():
    app = wx.App(False)
    frame = MainWindow(None, "wxSQL")
    app.MainLoop()

if __name__ == '__main__':
    main()
