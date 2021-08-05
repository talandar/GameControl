import wx


class PlaylistEditFrame(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "This page for editing/formatting playlists", (20, 20))

    def update(self, args):
        """Input to this method is the json form of the get_file_data from the music module"""
        self.output.SetValue(args)