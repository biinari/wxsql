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

    def CreateWidgets(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        editor = QueryEditorCtrl(self, style=wx.TE_MULTILINE)
        vbox.Add(editor, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        self.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    frame = wx.Frame(None, title="Query Editor", size=(600, 400))
    panel = QueryEditorPanel(frame)
    frame.Show(True)
    app.MainLoop()
