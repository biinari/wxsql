#!/usr/bin/env python
""" MySQL Query Editor control. """

import wx

class QueryEditorCtrl(wx.TextCtrl):
    """ MySQL Query Editor control. """

    def __init__(self, *args, **kwargs):
        """ Create MySQL Query Editor Control """
        wx.TextCtrl.__init__(self, *args, **kwargs)

class QueryEditorPanel(wx.Panel):
    """ MySQL Query Editor panel """

    def __init__(self, *args, **kwargs):
        """ Create MySQL Query Editor panel. """
        wx.Panel.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        """ Add and layout widgets. """
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
