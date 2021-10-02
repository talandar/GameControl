import asyncio
from music.music_module import MusicModule
import websockets
import json
import recap.recap_manager as recap
from message import generate_message, split_message
import yaml

"""https://websockets.readthedocs.io/en/stable/intro.html"""


class ControlServer(object):

    def __init__(self):
        self.config = self._load_config()
        self.music_module = MusicModule(self.config["music_root"])

    def _load_config(self):
        with open("server_config.yaml", "r") as f:
            config = yaml.safe_load(f)
            print("Loaded Config:")
            print(config)
            return config

    async def _receive_loop(self, websocket, path):
        while True:
            message_string = await websocket.recv()
            print(f'message received: {message_string}')
            message = json.loads(message_string)

            module, args = split_message(message)
            response = generate_message("ACK", "ACK")

            print(f"message to module {module}, with args \"{args}\"")

            if module == "RECAP":
                formatted_recap = recap.format_recap(args)
                response = generate_message("RECAP", formatted_recap)
            if module == "MUSIC" or module == "PLAYLIST":  # TODO
                module_return = self.music_module.action(args)
                if module_return:
                    response = generate_message("PLAYLIST", module_return)
            if module == "MEDIA":  # TODO
                print(f"Display image: {args}")
            if module == "LIGHT":  # TODO
                print(f"Adjust lights: {args}")
            if module == "SHARE":  # TODO
                print(f"Share file via discord: {args}")
            if module == "ECHO":
                print("Echoing message back to sender")
                response = message
            await websocket.send(json.dumps(response))

    def start_listening(self):
        self._listener = websockets.serve(self._receive_loop, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(self._listener)
        asyncio.get_event_loop().run_forever()


def main():
    svr = ControlServer()
    svr.start_listening()
    print("start_listening is blocking, we don't get here")


if __name__ == '__main__':
    main()
