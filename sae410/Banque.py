import asyncio
import nats

balancesheet = {
    "FR3810096000306954212365Y38": 50000,
    "FR2014508000307588774255A82": 23624
}


async def cb(msg):
    global balancesheet
    compte = msg.data.decode().split(',')[0]
    prix = int(msg.data.decode().split(',')[1])

    if compte not in balancesheet:
        await msg.respond("ECHEC : Ce compte client n'existe pas".encode())
        return
    if balancesheet[compte] <= prix:
        print(f"ECHEC : Solde insuffisant sur compte {compte}.")
        await msg.respond("ECHEC : Solde insuffisant".encode())
        return
    balancesheet[compte] -= prix
    print(f"SUCCES :Somme preleve sur compte {compte}. \nSolde restant : {balancesheet[compte]}")
    await msg.respond("SUCCES :Somme preleve".encode())


async def banque():
    nc = await nats.connect("nats://172.31.176.123:4222")       # Modifier l'IP en fct du Serveur
    sub = await nc.subscribe("pay", cb=cb)

    while True:
        await asyncio.sleep(1)


asyncio.run(banque())