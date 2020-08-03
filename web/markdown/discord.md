> July 4, 2020

# Simple Discord Chat Bot Graphical User Interfaces
[github](repo://discord-bot-ui) [demo](demo://discord-ui)
---

Though the `discord` chatbot api is rather limited, there is a surprising amount of things you can do with bots.  I recently discovered that it is possible to make simple graphical user interfaces with discord chat bots.  By exploiting chat reactions, message editing, and embeds, one can create rudimentary buttons.  In this tutorial, we will implement a bot that displays server status for a set of servers.

![img](/img/bot_final.png)

## Prerequisites

This tutorial assumes that you already know how to set up a discord bot.  If not, I'd suggest reading some tutorials before continuing.  Don't worry.  There are many helpful starter guides out there, and the process isn't too complicated.  

This tutorial uses `python3` + `discord.py` as our development framework.  Assuming you have `python3` and `pip` installed correctly, the `discord.py` module can be installed with the following command:
```sh
python3 -m pip install discord.py
```

## Some Skeleton Code

Let's start by writing a "ping bot", which responds with `pong` when the command `!ping` is received.  This will allow us to test our setup and serve as some skeleton code to work off of.  Here is an implementation of the ping bot:
```python
import discord
from discord.ext import commands

TOKEN = "<Insert your API Token HERE>"

bot = commands.Bot(command_prefix="!")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

bot.run(TOKEN)
```
Attach the bot to your server's channel and run the script.  If all goes well, you should now be able to interact with the bot.

![ping_bot](/img/ping_bot.png)

## Embeds

If you've frequented discord, odds are you've already seen an embed.  An embed is essentially a way to encapsulate text and images in a box.  We will use embeds for this bot because they look sort of like application windows inside the chat.  This may help the user recognize our bots response as an interactive UI.  We can add an embed to our bot with the following modifications.  Note that we've moved on from the `ping` bot, and are now building the server status bot.
```python
@bot.command()
async def status(ctx):
    message = await ctx.send(embed=discord.Embed(
        title="Server Status",
        description="""
\`\`\`diff
+ Server is UP
- Server is DOWN
\`\`\`
"""
    ))
```
Now the bot's response should look something like this:

![image_bot](/img/embed\.png)

## Adding Reactions

We are going to exploit the way that reactions look and act in discord to create buttons.  We will do this by add reacts to our embed to create "buttons" and then wait for the user to click the reactions and respond accordingly.  The following lines of code add left-arrow, refresh, and right arrow buttons respectively.

```python
await message.add_reaction('\u25c0')
await message.add_reaction('🔄')
await message.add_reaction('\u25b6')
```
![image_thingy](/img/bot_reactions.png)

## Responding to Button Presses

> The following code snippets are psuedocode that outline what we need to do.  For the actual implementation, skip to the end of this section.

### Detecting Button Presses

The following code waits for a reaction in a loop.  If there is no reaction in `60s`, we stop listening for responses:

```python
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        except TimeoutError:
            break
```

The emoji pressed is stored in `reaction.emoji`.  From that we can determine how to respond.  Note that we must check to make sure that the reaction was not created by the bot.

```python
        if str(user) != "botname#xxxx":
            if reaction.emoji == "\u25c0":
                # < pressed
                pass
            if reaction.emoji == "🔄":
                # refresh pressed
                pass
            if reaction.emoji == "\u25b6":
                # > pressed
                pass
```
### Changing the Message

Once we detect a reaction from the user and determine the emoji, we need to update our message appropriately.  We can edit messages using `message.update` like so.

```python
await message.edit(embed=discord.Embed(
                title="Server Status - {0}".format(server),
                description="""
\`\`\`diff
+ Server is UP
\`\`\`
            """
            ))
```

### Finishing Touches

After we've processed the "button" click, we need to remove the user's reaction so that they can press the button again.  

```python
await message.remove_reaction(reaction.emoji, user)
```

Finally, after we exit the loop as a result of timeout, we should remove the "buttons" so that the user knows that the `UI` is no longer active.

```python
await message.clear_reactions()
```

## Putting It All Together

```python
@bot.command()
async def status(ctx):

    servers = {"Google": "UP", "Yahoo": "DOWN", "Bing": "UP"}

    message = await ctx.send(embed=discord.Embed(
        title="Server Status - Google",
        description="""
\`\`\`diff
+ Server is UP
\`\`\`
"""
    ))

    await message.add_reaction('\u25c0')
    await message.add_reaction('🔄')
    await message.add_reaction('\u25b6')

    i = 0
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0)
        except TimeoutError:
            break

        if str(user) != "shopkeeper#4781":
            if reaction.emoji == "\u25c0":
                i += 1
            if reaction.emoji == "🔄":
                pass
            if reaction.emoji == "\u25b6":
                i -= 1
            i %= 3

            server = list(servers.keys())[i]
            await message.edit(embed=discord.Embed(
                title="Server Status - {0}".format(server),
                description="""
            \`\`\`diff
{0} Server is {1}
            \`\`\`
            """.format("+" if servers[server] == "UP" else "-", servers[server])
            ))

            await message.remove_reaction(reaction.emoji, user)

    await message.clear_reactions()
```
The end result looks something like this:
![img](/img/bot_final.png)

## Limitations and Extensions

If you look carefully at the example code, you'll notice that the bot never actually checks if the servers are actually up.  Because this example meant to be illustrative of simple discord chat bot user interfaces, I decided to leave the logic of checking the server status out.  I'll leave it as a possible excercise for the reader to implement this functionality.

Also, the servers presented in this example `[google, yahoo, bing]` are probably not what discord users would likely be interested in.  Feel free to replace them with something more important if you feel so inclined.
