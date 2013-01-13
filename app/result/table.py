#!/usr/bin/env python
"""
Result table view.
"""

import wx
from functools import partial
from test.frame import TestFrame

class ResultTablePanel(wx.Panel):
    """ Result table panel. """

    grid = None
    sort_column = None
    sort_ascending = True
    data = []
    headers = []

    def __init__(self, *args, **kwargs):
        """ Create Result table panel. """
        wx.Panel.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        """ Add and layout widgets. """
        pass

    def set_data(self, headers, data):
        """ Display data in table with description used for row headers. """
        if self.grid == None:
            self.grid = wx.GridSizer(len(data) + 1, len(headers), 1, 1)
        i = 0
        self.headers = []
        self.data = []
        for header in headers:
            self.headers.append(header)
            column = wx.Button(self, label=header[0])
            self.grid.Add(column, 0, wx.ALIGN_CENTER)
            column.Bind(wx.EVT_BUTTON, partial(self.on_column_button, i))
            i += 1
        for row in data:
            self.data.append(row)
            for column in row:
                self.grid.Add(wx.StaticText(self, label=str(column)), 0, wx.ALIGN_CENTER)
        self.SetSizer(self.grid)
        self.Fit()

    def sort_data(self, column, ascending=True):
        """ Sort by nth column in ascending or descending order. """
        self.sort_column = column
        self.sort_ascending = ascending
        self.data.sort(key=lambda item: item[column], reverse=(not ascending))
        self.grid.Clear(deleteWindows=True)
        self.set_data(self.headers, self.data)

    def on_column_button(self, column, event):
        if self.sort_column == column:
            ascending = not self.sort_ascending
        else:
            ascending = True
        self.sort_data(column, ascending)

def main():
    app = wx.App(False)
    frame = TestFrame(None, title="Results Table", size=(600, 400))
    panel = ResultTablePanel(frame)
    frame.Show(True)

    from app.db.mysql import DB
    db = DB()
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM `test`.`person`')
    description = cursor.description
    data = cursor.fetchall()
    cursor.close()
    panel.set_data(description, data)

    app.MainLoop()

if __name__ == '__main__':
    main()
