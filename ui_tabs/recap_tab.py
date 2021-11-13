import wx
from message import generate_message


class RecapFrame(wx.Panel):
    def __init__(self, parent, queue):
        wx.Panel.__init__(self, parent)
        self.queue = queue
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.input = wx.TextCtrl(self, style=(wx.TE_MULTILINE + wx.HSCROLL + wx.TE_PROCESS_TAB))
        self.btn = btn = wx.Button(self, label="Format Recap")
        self.output = wx.TextCtrl(self, style=(wx.TE_MULTILINE + wx.HSCROLL + wx.TE_READONLY))
        self.sizer.Add(self.input, 1, wx.EXPAND)
        self.sizer.Add(self.btn, 0, wx.EXPAND)
        self.sizer.Add(self.output, 1, wx.EXPAND)
        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        btn.Bind(wx.EVT_BUTTON, self.onButton)

    def onButton(self, event):
        """
        Runs the thread
        """
        msg = generate_message("RECAP", self.input.GetValue())
        self.queue.put(msg)

    def update(self, args):
        self.output.SetValue(args)
