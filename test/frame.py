"""
Quick Test frame.
"""

import wx

class TestFrame(wx.Frame):
    """ Quick Test frame. """

    def __init__(self, *args, **kwargs):
        """ Create Test frame. """
        wx.Frame.__init__(self, *args, **kwargs)
        self.create_menu()

    def create_menu(self):
        """ Setup menu bar. """
        file_menu = wx.Menu()
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Quit")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

    def on_exit(self, event):
        """ Exit the application. """
        self.Close(True)
