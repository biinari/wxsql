#!/usr/bin/env python
"""
Result table view.
"""

import wx
from test.frame import TestFrame

class ResultTablePanel(wx.Panel):
    """ Result table panel. """

    def __init__(self, *args, **kwargs):
        """ Create Result table panel. """
        wx.Panel.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        """ Add and layout widgets. """
        pass

    def set_data(self, description, data):
        """ Display data in table with description used for row headings. """
        self.grid = wx.GridSizer(len(data) + 1, len(description))
        self.SetSizer(self.grid)
        for heading in description:
            self.grid.Add(wx.Button(self, label=heading[0]))
        for row in data:
            for column in row:
                self.grid.Add(wx.StaticText(self, label=str(column)))

def main():
    app = wx.App(False)
    frame = TestFrame(None, title="Results Table", size=(600, 400))
    panel = ResultTablePanel(frame)

    from app.db.mysql import DB
    db = DB()
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM `test`.`person`')
    description = cursor.description
    data = cursor.fetchall()
    cursor.close()
    panel.set_data(description, data)

    frame.Show(True)
    frame.SetFocus()
    app.MainLoop()

if __name__ == '__main__':
    main()
