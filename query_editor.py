#!/usr/bin/env python

import wx

class QueryEditorCtrl(wx.TextCtrl):

    """ SQL Query Editor Control """
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, *args, **kwargs)

class QueryEditorPanel(wx.Panel):

    """ SQL Query Editor Panel """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.CreateWidgets()
        self.Show(True)

    def CreateWidgets(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        editor = QueryEditorCtrl(self, size=(600,400), style=wx.TE_MULTILINE)
        vbox.Add(editor, 0, wx.EXPAND)

class QueryEditorFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        panel = QueryEditorPanel(self)
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = QueryEditorFrame(None, title="Query Editor", size=(600, 400))
    app.MainLoop()
