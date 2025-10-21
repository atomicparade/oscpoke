import logging
import signal
import sys
import tomllib

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient


logger = logging.getLogger("oscpoke")


def on_sigint(sig, frame):
    logger.info("Received SIGINT; shutting down")
    sys.exit(0)


class OscPoke:
    def __init__(self, config):
        self.listen_port = int(config.get("listen_port", 8888))
        self.results_port = int(config.get("results_port", 8000))
        self.ping_address = config.get("ping_address", "/ping")
        self.ping_port = int(config.get("ping_port", 8888))
        self.ping_delay_sec = int(config.get("ping_delay_sec", 60))

        if self.listen_port < 0:
            logger.error("listen_port must be >= 0")
            sys.exit(1)

        if self.results_port < 0:
            logger.error("results_port must be >= 0")
            sys.exit(1)

        if (
            not isinstance(self.ping_address, str)
            or len(self.ping_address) == 0
            or self.ping_address[0] != "/"
        ):
            logger.error("ping_address must be a string beginning with '/'")
            sys.exit(1)

        if self.ping_port < 0:
            logger.error("ping_port must be >= 0")
            sys.exit(1)

        if self.ping_delay_sec < 1:
            logger.error("ping_delay_sec must be >= 1")
            sys.exit(1)

        self.client = SimpleUDPClient("0.0.0.0", self.results_port)

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/pong", self.osc_pong)

        self.server = ThreadingOSCUDPServer(
            ("0.0.0.0", self.listen_port), self.dispatcher
        )

        logger.info(f"listen_port:    {self.listen_port}")
        logger.info(f"results_port:   {self.results_port}")
        logger.info(f"ping_address:   {self.ping_address}")
        logger.info(f"ping_port:      {self.ping_port}")
        logger.info(f"ping_delay_sec: {self.ping_delay_sec}")

        self.server.serve_forever()

        # TODO: Take inventory of devices
        # TODO: Ping devices on interval

    def osc_pong(self, *args):
        print(args)
        # TODO: Record device pong


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    signal.signal(signal.SIGINT, on_sigint)

    try:
        with open("config.toml", "rb") as config_file:
            config = tomllib.load(config_file)
    except FileNotFoundError:
        logger.error("File config.toml does not exist")
        sys.exit(1)

    oscpoke = OscPoke(config)
