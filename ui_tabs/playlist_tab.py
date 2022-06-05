from message import generate_message
import wx


class PlaylistEditFrame(wx.Panel):
    def __init__(self, parent, queue):
        wx.Panel.__init__(self, parent)
        self.queue = queue
        self.request_data()
        #wx.StaticText(self, -1, "This page for editing/formatting playlists", (20, 20))

    def request_data(self):
        msg = generate_message("PLAYLIST", generate_message("DATA","NOOP"))
        self.queue.put(msg)

    def update(self, args):
        """Input to this method is the json form of the get_file_data from the music module"""

        # number of columns = 1 for name, plus one for each playlist
        self.playlists = args["lists"]
        name_root = args["root"]
        num_columns = 1 + len(self.playlists)
        self.gridsizer = wx.GridSizer(cols=num_columns, vgap=1, hgap=2)
        self.outer_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.buttons_sizer = wx.BoxSizer()
        self.prev_page = wx.Button(self, label="<")
        self.new_playlist = wx.Button(self, label="New Playlist")
        self.next_page = wx.Button(self, label=">")
        self.buttons_sizer.Add(self.prev_page, 1)
        self.buttons_sizer.Add(self.new_playlist, 1, wx.HORIZONTAL)
        self.buttons_sizer.Add(self.next_page, 1)
        self.outer_sizer.Add(self.buttons_sizer, 1, wx.EXPAND)
        self.outer_sizer.AddSpacer(10)
        self.outer_sizer.Add(self.gridsizer, 1, wx.EXPAND)
        self.file_list = args["files"]
        self.gridsizer.Add(wx.StaticText(self, -1, "File Name"))
        for playlist in self.playlists:
            self.gridsizer.Add(wx.StaticText(self, -1, playlist))

        for filename, filedata in self.file_list.items():
            display_name = filename[len(name_root):]
            self.gridsizer.Add(wx.StaticText(self, -1, display_name))
            for playlist in self.playlists:
                in_list = filedata[playlist]
                self.gridsizer.Add(wx.StaticText(self, -1, f"{in_list}"))

        self.SetSizer(self.outer_sizer)
        self.SetAutoLayout(1)
        self.outer_sizer.Fit(self)

