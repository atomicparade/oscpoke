import pythonosc
import tomllib


def osc_pong(_addr):
    pass


if __name__ == "__main__":
    with open("config.toml", "r") as config_file:
        config = tomllib.load(config_file)

    client = pythonosc.udp_client.SimpleUDPClient("localhost", 8888)

    dispatcher = pythonosc.dispatcher.Dispatcher()
    dispatcher.map("/pong", osc_pong)

    server = pythonosc.osc_server.ThreadingOSCUDPServer(("0.0.0.0", 8888), dispatcher)

    server.server_forever()
