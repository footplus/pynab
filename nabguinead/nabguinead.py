import datetime
import random
import sys

from nabcommon.nabservice import NabRandomService
from nabcommon.typing import NabdPacket


class NabGuinead(NabRandomService):
    DAEMON_PIDFILE = "/run/nabguinead.pid"

    async def get_config(self):
        from . import models

        config = await models.Config.load_async()
        return (config.next_guinea, None, config.guinea_frequency)

    async def update_next(self, next_date, next_args):
        from . import models

        config = await models.Config.load_async()
        config.next_guinea = next_date
        await config.save_async()

    async def perform(self, expiration, args, config):
        packet = (
            '{"type":"command",'
            '"sequence":[{"audio":["nabguinead/wheek/*"], "choreography":"urn:x-chor:streaming"}],'
            '"expiration":"' + expiration.isoformat() + '"}\r\n'
        )
        self.writer.write(packet.encode("utf8"))
        await self.writer.drain()

    def compute_random_delta(self, frequency):
        return (256 - frequency) * 60 * (random.uniform(0, 255) + 64) / 128

    async def process_nabd_packet(self, packet: NabdPacket):
        if (
            packet["type"] == "asr_event"
            and packet["nlu"]["intent"] == "nabguinead/guinea"
        ):
            now = datetime.datetime.now(datetime.timezone.utc)
            expiration = now + datetime.timedelta(minutes=1)
            await self.perform(expiration, None, None)
        elif (
            packet["type"] == "rfid_event"
            and packet["app"] == "nabguinead"
            and packet["event"] == "detected"
        ):
            now = datetime.datetime.now(datetime.timezone.utc)
            expiration = now + datetime.timedelta(minutes=1)
            await self.perform(expiration, None, None)


if __name__ == "__main__":
    NabGuinead.main(sys.argv[1:])
