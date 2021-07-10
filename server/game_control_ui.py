import asyncio
import websockets
import json
import wx
from threading import Thread
from pubsub import pub
import queue
from message import generate_message, split_message


class NotebookWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Gameroom Control")
        p = wx.Panel(self)
        self.notebook = wx.Notebook(p)
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        p.SetSizer(sizer)
        


class RecapFrame(wx.Panel):
    def __init__(self, parent, queue):
        wx.Panel.__init__(self, parent)
        self.queue = queue
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.displayLbl = wx.StaticText(self, label="Amount of time since thread started goes here")
        self.btn = btn = wx.Button(self, label="Start Thread")
        self.sizer.Add(self.displayLbl, 1, wx.EXPAND)
        self.sizer.Add(self.btn, 0, wx.EXPAND)
        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        btn.Bind(wx.EVT_BUTTON, self.onButton)

    def onButton(self, event):
        """
        Runs the thread
        """
        msg = generate_message("RECAP", "TEMP")
        self.queue.put(msg)
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        #btn.Disable()

    def update(self, args):
        self.displayLbl.SetLabel("Thread Finished!")


class PlaylistEditFrame(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, "This page for editing/formatting playlists", (20, 20))


class WebsocketThread(Thread):

    def __init__(self, ui_main, queue):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.stop = False
        self.ui = ui_main
        self.queue = queue
        print("about to start thread")
        self.start()

    def shutdown(self):
        self.stop = True

    def run(self):
        loop = asyncio.new_event_loop()  # loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())
        loop.close()

    async def _run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            print("socket connected")
            self.websocket = websocket
            await self.message_loop(websocket)

    async def message_loop(self, websocket):
        while not self.stop:
            try:
                message = self.queue.get(block=True, timeout=10)
                print(f"got {message} from queue")
            except queue.Empty:
                # no data this time, that's fine.  pump out a keepalive message
                message = generate_message("ECHO", "KEEPALIVE")
            await websocket.send(json.dumps(message))
            return_message = await websocket.recv()
            print(f"got return message: {return_message}")
            return_message = json.loads(return_message)
            wx.CallAfter(pub.sendMessage, "update", msg=return_message)


class ControlUI(object):
    modules = {}

    def __init__(self):
        self.app = wx.App()
        self.queue = queue.Queue()
        self.notebook_frame = NotebookWindow()
        self.websocket_thread = WebsocketThread(self.notebook_frame, self.queue)
        pub.subscribe(self.updateDisplay, "update")
        print("past thread creation")
        self.notebook_frame.Show()
        self.recap = RecapFrame(self.notebook_frame.notebook, self.queue)
        self._add_page("RECAP", self.recap, "Recap", True)
        self.playlist_edit = PlaylistEditFrame(self.notebook_frame.notebook)
        self._add_page("MUSIC", self.playlist_edit, "Playlist Edit")
        self.app.MainLoop()
        print("out of main loop")
        self.websocket_thread.shutdown()

    def _add_page(self,  module, page, title, selected=False):
        self.notebook_frame.notebook.AddPage(page, title, selected)
        self.modules[module] = page


    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        print("Got update display")
        module, args = split_message(msg)
        page = self.modules.get(module, None)
        if page:
            page.update(args)



if __name__ == '__main__':
    control = ControlUI()
    print('out of initializer')

    #asyncio.get_event_loop().run_until_complete(hello())
