# bot.py
import os
import random
import re

from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

client = commands.Bot(command_prefix='!')
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client.botinit = False
client.mdc = ''
client.dc = ''
client.prefix = '!'
# TODO: set manually
client.sendErrors = False
client.pollCount = 1;
client.nopes = [
    'nö',
    'ne',
    'nein',
    ':clown: :clown: :clown:',
    'Bruder muss los',
    'Abonniere jetzt MokruHD **GRATIS** mit Twitch Prime: http://twitch.tv/MoKruHD',
]

async def timestamp():
    now = datetime.now()
    dt_string = now.strftime('[%d.%m.%Y - %H:%M:%S] ')
    return dt_string

@client.event
async def on_ready():
    time = await timestamp()
    print(time+f'{client.user.name} hat sich mit Discord verbunden.')


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Ich bin Polly!\nDanke, dass du mich auf deinen Server eingeladen hast.\n"
                               "Um fortzufahren, schreib einfach !pollysetup in den Kanal, in dem du mich kontrollieren "
                               "willst!\n\nÜbrigens: Kanäle, auf die alle zugreifen können, sind da schlecht :).")
            time = await timestamp()
            print(time + "f'{client.user.name} ist einem Server beigetreten: "+ guild.name)
        break


@client.command(pass_context=True)
async def id(ctx):
    id = ctx.message.channel.id
    name = ctx.message.channel.name
    await ctx.send("Die ID des Kanals " + str(name) + " ist: " + str(id))


@client.command(pass_context=True)
@has_permissions(administrator=True)
async def pollysetup(ctx, *values):
    length = int(((values.__sizeof__()) - 24) / 8)
    data = []
    for i in range(0, length):
        data.append(str(values[i]))
    if client.botinit == False:
        if length > 1:
            client.mdc = data[0]
            client.dc = data[1]
            await ctx.send("Einrichtung ist abgeschlossen! Bitte benutze !polly help für weitere Anweisungen!")
            client.botinit = True
        elif client.mdc!='' and client.dc!='':
            await ctx.send("Einrichtung ist abgeschlossen! Bitte benutze !polly help für weitere Anweisungen!")
            client.botinit = True
        else:
            await ctx.send("Syntax: **!pollysetup** [*Mod-Channel-ID*] [*Poll-Channel-ID*]\n"
                           "Um die ID eines Kanals zu erhalten, nutze einfach !id.\n"
                           "Alternativ kannst du mit **!pollymdc** den Moderationskanal und mit **!pollydc** den Umfragekanal setzen!"
                           )
    else:
        await ctx.send(random.choice(client.nopes))

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def pollymdc(ctx):
    id = ctx.message.channel.id
    name = ctx.message.channel.name
    client.mdc = id
    await ctx.send("Der Kanal " + str(name) + " wurde als Moderationskanal gesetzt!")

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def pollydc(ctx):
    id = ctx.message.channel.id
    name = ctx.message.channel.name
    client.dc = id
    await ctx.send("Der Kanal " + str(name) + " wurde als Umfragekanal gesetzt!")

@client.command()
async def polly(ctx, *values):
    length = int(((values.__sizeof__()) - 24) / 8)
    # Process further inputs
    data = []
    for i in range(0, length):
        data.append(str(values[i]))
    # Append characters of *values to data
    if (client.botinit == True and str(ctx.message.channel.id) == str(client.mdc) and length > 0 and str(
            values[0]).lower() == "help" or str(values[0]).lower() == "-h" or str(values[0]).lower() == "hilfe"):
        channel = client.get_channel(int(client.dc))
        for i in range(0, length):
            data[i] = str(data[i]).lower()
        # Process data
        if (length > 1 and data[1] == "create"):
            if (length > 2 and (data[2] == "-c" or data[2] == "-color" or data[2] == "color" or data[2] == "c")):
                helper = discord.Embed(title='!polly create -c/-color "Farbwert"',
                                       description="Neben einer Liste vordefinierter Farbwerte kann man auch eigene Farbwerte für die Seitenleiste nutzen.\nHier können [normale, hexadezimale Farbwerte](https://www.google.com/search?q=hex+color+picker) genutzt werden.",
                                       color=15158332)
                helper.add_field(name='Vordefinierte Farbcodes:',
                                 value='red,green,blue,gold,orange,pink,purple,dark_purple,grey,dark_grey\nBeispiel: !polly create -c "red"',
                                 inline=False)
                helper.add_field(name='Eigene Farbcodes:',
                                 value='Erlaubt das Nutzen eigener Farben.\nBeispiel: !polly create -c "#FFFFFF"',
                                 inline=False)
                await ctx.send(embed=helper)
            elif (length > 2 and (data[2] == "-em" or data[2] == "-emoji" or data[2] == "em" or data[2] == "emoji")):
                helper = discord.Embed(title='!polly create -em/emoji "Emoji"',
                                       description='-em/-emoji muss immer mit einem folgenden -emtext/-emojitext genutzt werden. Beide zusammen definieren eine mögliche Antwortmöglichkeit, eine Mehrfachnutzung dieser Argumente ist also möglich.\nBeispiel: !polly create -em 👍 -emtext "Ja" -em 👎 -emtext "Nein"',
                                       color=15158332)
                await ctx.send(embed=helper)
            else:
                helper = discord.Embed(title="!polly create [Argument] [Wert]",
                                       description="Jedes Argument repräsentiert einen Modifier für das Quiz, wird dieser nicht gesetzt, so werden Standartwerte an seiner Stelle eingesetzt.\nListe an Argumenten:",
                                       color=15158332)
                helper.add_field(name='-t/-title "Titel"',
                                 value='Fügt einen Titel für die Umfrage hinzu.\nBeispiel: !polly create -t "Ist Mary cool?"',
                                 inline=False)
                helper.add_field(name='-c/-color "Farbwert"',
                                 value='Ändert die Farbe der Seitenleiste.\nFarbwerte finden sich bei !polly help create -c/-color.\nBeispiel: !polly create -c "red"',
                                 inline=False)
                helper.add_field(name='-img/-image "Bild-URL"',
                                 value='Fügt ein Bild in das Quiz hinzu.\nBeispiel: !polly create -img "https://picsum.photos/300.jpg"',
                                 inline=False)
                helper.add_field(name='-desc/-description "Beschreibung unter dem Titel"',
                                 value='Fügt der Umfrage einen Subtext hinzu, der mehr Informationen enthält.\nBeispiel: !polly create -desc "Hallo i bims lol"',
                                 inline=False)
                helper.add_field(name='-em/-emoji Emoji',
                                 value='Wählt für eine Antwortmöglichkeit einen Emoji aus.\nMehr Informationen finden sich bei "!polly help create -em/-emoji".\nBeispiel: !polly create -em 🤡',
                                 inline=False)
                helper.add_field(name='-emtext/-emojitext "Antworttext"',
                                 value='Definiert den Text einer Antwortmöglichkeit.\nBeispiel: !polly create -emtext "Ja"',
                                 inline=False)
                await ctx.send(embed=helper)
        elif (length > 1 and data[1] == "help"):
            helper = discord.Embed(title="Hilfe-Menü für Hilfe-Menü",
                                   description="Nein",
                                   color=15158332)
            helper.set_footer(text="bot created by cbxy - https://mwae.de",
                              icon_url="https://cdn.discordapp.com/avatars/241653148601548801/cbae080a322e562c20d5cfab52c63721.png?size=256")
            await ctx.send(embed=helper)
        else:
            helper = discord.Embed(title="Hilfe-Menü für Bot-Commands",
                                   description="Weitere Informationen zu den einzelnen Kommandos findest Du mit !polly help [Kommando] (z.B.: -!polly help create)",
                                   color=15158332)
            helper.set_footer(text="bot created by cbxy - https://mwae.de",
                              icon_url="https://cdn.discordapp.com/avatars/241653148601548801/210e642ff1b52daf6ae8ff3b8552efd0.png?size=256")
            helper.add_field(name="!polly help",
                             value="Öffnet das Hilfemenü",
                             inline=False)
            helper.add_field(name="!polly create",
                             value="Erstellt Umfragen",
                             inline=False)
            helper.add_field(name="!polly preview",
                             value="Testet Umfragen",
                             inline=False)
            helper.add_field(name="!pollysetup",
                             value="Tool zum Aufsetzen des Bots",
                             inline=False)
            helper.add_field(name="!polly senderrors",
                             value="Kontrolliert die Fehlerausgabe [WIP]",
                             inline=False)
            await ctx.send(embed=helper)

    elif (client.botinit == True and str(ctx.message.channel.id) == str(client.mdc) and length > 0 and (
            data[0] == "create" or data[0] == "-c" or data[0] == "erstellen")):
        channel = client.get_channel(int(client.dc))
        title = "Ups, irgendwer hat den Umfragetitel vergessen :]"
        desc = "Umfrage bereitgestellt von Polly"
        colorcode = 0
        hasImage = False
        fieldCount = 0
        emoji = []
        emojitext = []
        for i in range(1, int((length - 1) / 2) + 1):
            data[i * 2 - 1] = str(data[i * 2 - 1]).lower()
            if (data[i * 2 - 1] == "-t" or data[i * 2 - 1] == "-title" or data[i * 2 - 1] == "t" or data[
                i * 2 - 1] == "title"):
                title = data[i * 2]
            if (data[i * 2 - 1] == "-img" or data[i * 2 - 1] == "-image" or data[i * 2 - 1] == "img" or data[
                i * 2 - 1] == "image"):
                image = data[i * 2]
                hasImage = True
            if (data[i * 2 - 1] == "-desc" or data[i * 2 - 1] == "-description" or data[i * 2 - 1] == "desc" or data[
                i * 2 - 1] == "description"):
                desc = data[i * 2]
            if (data[i * 2 - 1] == "-em" or data[i * 2 - 1] == "-emoji" or data[i * 2 - 1] == "em" or data[
                i * 2 - 1] == "emoji"):
                fieldCount = fieldCount + 1
                emoji.append(data[i * 2])
            if (data[i * 2 - 1] == "-emtext" or data[i * 2 - 1] == "-emojitext" or data[i * 2 - 1] == "emojitext" or
                    data[i * 2 - 1] == "emtext"):
                emojitext.append(data[i * 2])
            if (data[i * 2 - 1] == "-color" or data[i * 2 - 1] == "color" or data[i * 2 - 1] == "-c" or data[
                i * 2 - 1] == "c"):
                color = data[i * 2]
                if (color == "rot" or color == "red"):
                    colorcode = 15158332
                elif (color == "grün" or color == "green"):
                    colorcode = 3066993
                elif (color == "blau" or color == "blue"):
                    colorcode = 3447003
                elif (color == "gold"):
                    colorcode = 15844364
                elif (color == "grau" or color == "grey"):
                    colorcode = 9807270
                elif (color == "dunkelgrau" or color == "dark grey" or color == "darkgrey" or color == "dark_grey"):
                    colorcode = 8359053
                elif (color == "lila" or color == "purple"):
                    colorcode = 10181046
                elif (color == "orange"):
                    colorcode = 15105570
                elif (color == "pink"):
                    colorcode = 16580705
                elif (re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(color)) == True or re.search(
                        r'(?:[0-9a-fA-F]{3}){1,2}$',
                        str(color)) == True):
                    colorcode = int(str(color).replace('#', ''),
                                    16)  # if hex color code convert to discord dec color and subtract #
                else:
                    colorcode = 0
        poll = discord.Embed(title=title,
                             description=desc,
                             color=colorcode)
        if hasImage:
            poll.set_image(url=image)
        poll.set_author(name="Poll #" + str(client.pollCount) + " | by Polly", url="https://mwae.de",
                        icon_url="https://cdn.discordapp.com/avatars/722092645555503114/7c373acca26bdcb11defa8f0123ddc48.png?size=128")
        poll.set_footer(text="bot created by cbxy - https://mwae.de",
                        icon_url="https://cdn.discordapp.com/avatars/241653148601548801/210e642ff1b52daf6ae8ff3b8552efd0.png?size=128")
        for i in range(0, fieldCount):
            poll.add_field(name=emoji[i], value=emojitext[i], inline=True)
        msg = await channel.send(embed=poll)
        await ctx.send("Umfrage '" + title + "' generiert!")
        if data[0] == "create" or data[0] == "-c" or data[0] == "erstellen":
            client.pollCount = client.pollCount + 1
            time = await timestamp()
            print(time + "Umfrage '" + title + "' erfolgreich erstellt")
        for j in range(0, fieldCount):
            await msg.add_reaction(emoji[j])

    elif (client.botinit == True and str(ctx.message.channel.id) == str(client.mdc) and length > 0 and (data[0] == "preview" or data[0] == "-prev" or data[0] == "testen")):
        channel = client.get_channel(int(client.mdc))
        title = "Ups, irgendwer hat den Umfragetitel vergessen :]"
        desc = "Umfrage bereitgestellt von Polly"
        colorcode = 0
        hasImage = False
        fieldCount = 0
        emoji = []
        emojitext = []
        for i in range(1, int((length - 1) / 2) + 1):
            data[i * 2 - 1] = str(data[i * 2 - 1]).lower()
            if (data[i * 2 - 1] == "-t" or data[i * 2 - 1] == "-title" or data[i * 2 - 1] == "t" or data[
                i * 2 - 1] == "title"):
                title = data[i * 2]
            if (data[i * 2 - 1] == "-img" or data[i * 2 - 1] == "-image" or data[i * 2 - 1] == "img" or data[
                i * 2 - 1] == "image"):
                image = data[i * 2]
                hasImage = True
            if (data[i * 2 - 1] == "-desc" or data[i * 2 - 1] == "-description" or data[i * 2 - 1] == "desc" or data[
                i * 2 - 1] == "description"):
                desc = data[i * 2]
            if (data[i * 2 - 1] == "-em" or data[i * 2 - 1] == "-emoji" or data[i * 2 - 1] == "em" or data[
                i * 2 - 1] == "emoji"):
                fieldCount = fieldCount + 1
                emoji.append(data[i * 2])
            if (data[i * 2 - 1] == "-emtext" or data[i * 2 - 1] == "-emojitext" or data[i * 2 - 1] == "emojitext" or
                    data[i * 2 - 1] == "emtext"):
                emojitext.append(data[i * 2])
            if (data[i * 2 - 1] == "-color" or data[i * 2 - 1] == "color" or data[i * 2 - 1] == "-c" or data[
                i * 2 - 1] == "c"):
                color = data[i * 2]
                if (color == "rot" or color == "red"):
                    colorcode = 15158332
                elif (color == "grün" or color == "green"):
                    colorcode = 3066993
                elif (color == "blau" or color == "blue"):
                    colorcode = 3447003
                elif (color == "gold"):
                    colorcode = 15844364
                elif (color == "grau" or color == "grey"):
                    colorcode = 9807270
                elif (color == "dunkelgrau" or color == "dark grey" or color == "darkgrey" or color == "dark_grey"):
                    colorcode = 8359053
                elif (color == "lila" or color == "purple"):
                    colorcode = 10181046
                elif (color == "orange"):
                    colorcode = 15105570
                elif (color == "pink"):
                    colorcode = 16580705
                elif (re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(color)) == True or re.search(
                        r'(?:[0-9a-fA-F]{3}){1,2}$',
                        str(color)) == True):
                    colorcode = int(str(color).replace('#', ''),
                                    16)  # if hex color code convert to discord dec color and subtract #
                else:
                    colorcode = 0
        poll = discord.Embed(title=title,
                             description=desc,
                             color=colorcode)
        if hasImage:
            poll.set_image(url=image)
        poll.set_author(name="Poll #" + str(client.pollCount) + " | by Polly", url="https://mwae.de",
                        icon_url="https://cdn.discordapp.com/avatars/722092645555503114/7c373acca26bdcb11defa8f0123ddc48.png?size=128")
        poll.set_footer(text="bot created by cbxy - https://mwae.de",
                        icon_url="https://cdn.discordapp.com/avatars/241653148601548801/210e642ff1b52daf6ae8ff3b8552efd0.png?size=128")
        for i in range(0, fieldCount):
            poll.add_field(name=emoji[i], value=emojitext[i], inline=True)
        msg = await channel.send(embed=poll)
        for j in range(0, fieldCount):
            await msg.add_reaction(emoji[j])


    elif (client.botinit == True and str(ctx.message.channel.id) == str(client.mdc) and (data[0] == "senderrors")):
        channel = client.get_channel(int(client.mdc))
        if client.sendErrors:
            channel.send("Errors turned off")
            client.sendErrors = False
        else:
            channel.send("Errors turned on")
            client.sendErrors = True

    elif (client.botinit == True and (data[0] == "stinkt")):
        await ctx.send(":c")

    elif (client.botinit == False):
        await ctx.send("Bitte nutze !pollysetup, um den Bot einzurichten!\n"
                       "Syntax: !pollysetup [Mod-Channel-ID] [Poll-Channel-ID]\n"
                       "Um die ID eines Kanals zu erhalten, nutze einfach !id."
                       )

    else:
        await ctx.send(random.choice(client.nopes))


@polly.error
async def polly_error(ctx, error):
    if client.sendErrors:
        ctx.send(error)
# WIP

@client.command()
async def test(ctx):
    await ctx.send("Moin")

@client.command()
async def mary(ctx):
    await ctx.send("Ich wurde gezwungen:");
    await ctx.send("https://open.spotify.com/user/nuwvuv9i3e8582vtzeba0as8i?si=qp-CKa3RTN69gQ1shMS8Mg")
    
client.run(TOKEN)
