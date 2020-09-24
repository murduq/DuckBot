import random, asyncio, time
from discord.ext.commands import Bot
from discord import Game, File
from os import path

token = open("tokenFile.txt", 'r')
T = token.readlines()
BOT_PREFIX = ("?", "!")
TOKEN = T[0]
client = Bot(command_prefix=BOT_PREFIX)

#########################################################################
#                             GLOBAL STORAGE                            #
#########################################################################

game = open("gameList.txt", 'a+')
show = open("showList.txt", 'a+')
game.close()
show.close()
COW_ID = int(T[1])
DUQ_ID = int(T[2])
UWU_LIST = ('UwU', 'OwO', 'TwT', '>w<', '^-^', 'ÒwÓ', '♡w♡', '>_<', 'XwX')

#########################################################################
#                               COMMANDS                                #
#########################################################################

# Help command
@client.command(name='helpme')
async def helpme(context):
    await context.send('?help, ?8ball, ?coinflip, ?random, ?add, ?delete, ?list')

# Magic 8-ball command
@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond",
                aliases=['eight_ball', "eightball", '8-ball'])
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no.',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Ask Cow'
    ]
    choice = random.randint(0,len(possible_responses)-1)
    await context.send(possible_responses[choice] + ". " + context.message.author.mention)

# Square number command
@client.command(name='sq',
                description='Responds with the number squared',
                brief='squares a number')
async def square(context, number):
    num_squared = (int(number) * int(number))
    await context.send(str(number) + " squared is " + str(num_squared))

# Coin flip command
@client.command(name='coinflip')
async def coin_flip(context):
    h = "Heads"
    t = "Tails"
    flip = int(random.random()*10)
    if flip<5:
        result = h
    elif flip>=5:
        result = t

    await context.send("Magic bot-coin says: " + str(result))

# Picker command
@client.command(aliases=['pick', 'choose', 'pickforme', 'decide', 'random'])
async def picker(context, *args):
    game = open("gameList.txt", 'r')
    show = open("showList.txt", 'r')
    try:
        l = eval(args[0]).read()
        print(l.splitlines())
        await context.send("I choose... " + random.choice(l.splitlines()))
        pass
    except:
        await context.send("I choose... " + random.choice(args))
        pass
    
# Add game/show to list
@client.command(name='add')
async def add(context):
    #TODO: Input validation (check for dupes)
    game = open("gameList.txt", 'a+')
    show = open("showList.txt", 'a+')
    x = context.message.content.split(' ', 2)
    eval(x[1]).write(x[2] + '\n')
    eval(x[1]).close()
    await context.send("Added " + x[2].title() + " to " + x[1].title() + 's')

# Remove game/show from list
@client.command(aliases=['del', 'delete'])
async def remove(context):
    game = open("gameList.txt", 'r')
    show = open("showList.txt", 'r')
    x = context.message.content.split(' ', 2)
    print("attempting to remove " + x[2])
    objList = eval(x[1]).read().splitlines()
    objList.remove(x[2])
    with open(eval(x[1]).name, 'w+') as f:
        f.write('\n'.join(objList) + '\n') 
    await context.send(x[2].title() + ' removed from ' + x[1].title() + 's')
    eval(x[1]).close()

# Display list
@client.command(name='list')
async def list(context,l):
    #TODO: input validation
    games = open("gameList.txt", 'r')
    shows = open("showList.txt", 'r')
    await context.send(eval(l).read())
    eval(l).close()

# numbers to remember
@client.command()
async def deaths(context, game):
    if game == 'ds3':   #DARK SOULS 3
        await context.send("123 deaths")
    elif game == 'ds2': #DARK SOULS 2
        await context.send("309 deaths. But like half of those don't count.")
    elif game == 'ds1': #DARK SOULS 1
        await context.send("33. so far.")
    elif game == 'ds3sl1': #DARK SOULS 3 SL1
        await context.send("29 deaths")

# bae TODO: read from bae channels?
@client.command()
async def bae(context):
    if(context.author.id == COW_ID):
        print('cow')
        b = 'cowbae2.jpg'
    elif(context.author.id == DUQ_ID):
        print()
        b = 'duqbae2.jpg'
    await context.send("Finding your bae...")
    time.sleep(1)
    await context.send(file=File(b))

# owo aka what is wrong with me
@client.command()
async def owo(context, *msgl):
    msg=''
    for x in msgl:
        msg += ' ' + x
    print(msg)
    await context.send(msg.replace('r', 'w').replace('l', 'w') + " ~ " + random.choice(UWU_LIST))

# TODO: HEADPAT COMMAND :)
@client.command()
async def headpat(context):
    await context.send("https://tenor.com/view/big-hero6-baymax-there-there-patting-head-pat-head-gif-4086973")

#########################################################################
#                               EVENTS                                  #
#########################################################################

# confirms login in terminal
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="with the meatbags"))    
    print("Logged in as " + client.user.name)

@client.event
async def on_message(message):
    if message.attachments:
        print(message.attachments)
        
    pic_ext = ['.jpg','.png','.jpeg']
    for ext in pic_ext:
        if (message.content.endswith(ext)):
            print("succ")
    await client.process_commands(message)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers: ")
        for server in client.guilds:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)