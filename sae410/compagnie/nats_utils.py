# nats_utils.py
import asyncio
from nats.aio.client import Client as NATS

async def request_message(subject, message, servers, timeout=1):
    nc = NATS()
    await nc.connect(servers)

    try:
        response = await nc.request(subject, message.encode(), timeout=timeout)
        return response.data.decode()
    except Exception :
        return None
    finally:
        await nc.drain()
        await nc.close()