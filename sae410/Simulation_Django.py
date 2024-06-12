import asyncio
import nats

async def cb(msg):
    print(msg.data.decode())


async def pay(numero_compte,montant):
    nc = await nats.connect("nats://172.31.176.123:4222")

    msg = await nc.request("pay",f"{numero_compte},{montant}".encode())
    print(msg.data)

    await nc.close()

asyncio.run(pay("FR3810096000306954212365Y38", 1000))