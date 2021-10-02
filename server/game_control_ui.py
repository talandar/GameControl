import asyncio
import websockets
import json
import wx
from threading import Thread
from pubsub import pub
import queue
import yaml
from message import generate_message, split_message
from ui_tabs import recap_tab, playlist_tab


class NotebookWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Gameroom Control")
        p = wx.Panel(self)
        self.notebook = wx.Notebook(p)
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        p.SetSizer(sizer)


class WebsocketThread(Thread):

    def __init__(self, ui_main, queue, server_connection_string):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.stop = False
        self.ui = ui_main
        self.queue = queue
        self._connection_string = server_connection_string
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
        async with websockets.connect(self._connection_string) as websocket:
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
        config = self._load_config()
        self.app = wx.App()
        self.queue = queue.Queue()
        self.notebook_frame = NotebookWindow()
        self.websocket_thread = WebsocketThread(self.notebook_frame, self.queue, config["server_uri"])
        pub.subscribe(self.updateDisplay, "update")
        print("past thread creation")
        self.notebook_frame.Show()
        self.recap = recap_tab.RecapFrame(self.notebook_frame.notebook, self.queue)
        self._add_page("RECAP", self.recap, "Recap", False)
        self.playlist_edit = playlist_tab.PlaylistEditFrame(self.notebook_frame.notebook, self.queue)
        self._add_page("PLAYLIST", self.playlist_edit, "Playlist Edit", True)
        self.app.MainLoop()
        print("out of main loop")
        self.websocket_thread.shutdown()

    def _load_config(self):
        with open("ui_config.yaml", "r") as f:
            config = yaml.safe_load(f)
            print("Loaded Config:")
            print(config)
            return config

    def _add_page(self,  module, page, title, selected=False):
        self.notebook_frame.notebook.AddPage(page, title, selected)
        self.modules[module] = page

    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        module, args = split_message(msg)
        page = self.modules.get(module, None)
        if page:
            page.update(args)
        else:
            if module != "ACK" and module != "ECHO":
                print(f"Unknown message: {msg}")


if __name__ == '__main__':
    control = ControlUI()
