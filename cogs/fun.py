import discord

import asyncio
import requests

import cogs.utils.checks as checks


from discord.ext import commands

from random import choice, randint, random

from .utils.yomama import getyomum
from .utils.roasts import getroast
from .utils.compliment import getcompliment
from .utils.barter import Piglin


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._task = {}
        self.deletedMsg = {}

    async def on_message_delete(self, message):
        self.deletedMsg[message.channel.id] = message

        async def deleteTask(channelId):
            del self.deleteMsg[channelId]
        if self._task.get(message.channel.id, None):
            self._task[message.channel.id].cancel()
        self._task[message.channel.id] = self.bot.loop.create_task(deleteTask(message.channel.id))

    @commands.command(aliases=["fs"])
    async def findseed(self, ctx):
        """`Test your Minecraft RNG, but in a bot command`"""
        rigged_findseed = {
            564610598248120320: 90000
        }

        if ctx.author.id in rigged_findseed:
            total_eyes = rigged_findseed[ctx.author.id]
        else:
            total_eyes = sum([1 for i in range(12) if randint(1, 10) == 1])
        await ctx.reply(
            f"{(ctx.message.author.mention)} -> your seed is a {total_eyes} eye"
        )

    @commands.command(aliases=["vfindseed", "visualfindseed", "vfs"])
    async def findseedbutvisual(self, ctx):
        """`Test your luck in Minecraft but visual.`"""

        emojis = {
            "{air}": "<:empty:854498044942352414>",
            "{frame}": "<:portal:854498112982351883>",
            "{eye}": "<:eye:854498044496969729>",
            "{end_portal}": "<:endportal:854498044426977301>",
            "{lava}": "<a:lava:854498074121994260>",
        }

        eyes = ["{eye}" if randint(1, 10) == 1 else "{frame}" for i in range(12)]
        eye_count = sum([1 for i in eyes if i == "{eye}"])

        # rig stuff
        # rig is capped at 12 no matter what
        rigged = {564610598248120320: 12}
        if ctx.author.id in rigged:
            rig = rigged[ctx.author.id]
            # cap rig
            if rig >= 12:
                eye_count, rig = (12,) * 2
                eyes = ["{eye}"] * 12
            elif rig <= 0:
                eye_count, rig = (0,) * 2
                eyes = ["{frame}"] * 12
            # rig loop
            while eye_count != rig:
                for i in range(len(eyes)):
                    if eye_count == rig:
                        break
                    if (
                        eyes[i] == "{frame}"
                        and randint(1, 10) == 1
                        and (eye_count < rig and eye_count != rig)
                    ):
                        eyes[i] = "{eye}"
                        eye_count += 1
                    elif eyes[i] == "{eye}" and (eye_count > rig and eye_count != rig):
                        eyes[i] = "{frame}"
                        eye_count -= 1

        # "render" portal
        sel_eye = 0
        portalframe = ""
        for row in range(5):
            for col in range(5):
                if ((col == 0 or col == 4) and (row != 0 and row != 4)) or (
                    (row == 0 or row == 4) and (col > 0 and col < 4)
                ):
                    sel_eye += 1
                    portalframe += eyes[sel_eye - 1]
                elif (col != 0 or col != 4) and (col > 0 and col < 4):
                    portalframe += "{end_portal}" if eye_count >= 12 else "{lava}"
                else:
                    portalframe += "{air}"
            portalframe += "\n"

        # replace placeholder with portal frame emoji
        for placeholder in emojis.keys():
            portalframe = portalframe.replace(placeholder, emojis[placeholder])

        e = discord.Embed(
            title="findseed",
            description=f"Your seed is a **{eye_count}** eye: \n\n{portalframe}",
            color=discord.Colour(0x38665E),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.reply(embed=e)

    @commands.command(aliases=["vfindseedbutpipega", "visualfindseedbutpipega", "vfsbp"])
    async def findseedbutvisualbutpipega(self, ctx):
        """`Test your luck in Minecraft but visual, and pipega?.`"""

        emojis = {
            "{air}": "<:empty:854498044942352414>",
            "{frame}": "<:pipega:855154384047964170>",
            "{eye}": "<:piog:855154383847030794>",
            "{end_portal}": "<:soapiog:855154383984787540>",
            "{lava}": "<:empty:854498044942352414>",
        }

        eyes = ["{eye}" if randint(1, 10) == 1 else "{frame}" for i in range(12)]
        eye_count = sum([1 for i in eyes if i == "{eye}"])

        # rig stuff
        # rig is capped at 12 no matter what
        rigged = {564610598248120320: 12}
        if ctx.author.id in rigged:
            rig = rigged[ctx.author.id]
            # cap rig
            if rig >= 12:
                eye_count, rig = (12,) * 2
                eyes = ["{eye}"] * 12
            elif rig <= 0:
                eye_count, rig = (0,) * 2
                eyes = ["{frame}"] * 12
            # rig loop
            while eye_count != rig:
                for i in range(len(eyes)):
                    if eye_count == rig:
                        break
                    if (
                        eyes[i] == "{frame}"
                        and randint(1, 10) == 1
                        and (eye_count < rig and eye_count != rig)
                    ):
                        eyes[i] = "{eye}"
                        eye_count += 1
                    elif eyes[i] == "{eye}" and (eye_count > rig and eye_count != rig):
                        eyes[i] = "{frame}"
                        eye_count -= 1

        # "render" portal
        sel_eye = 0
        portalframe = ""
        for row in range(5):
            for col in range(5):
                if ((col == 0 or col == 4) and (row != 0 and row != 4)) or (
                    (row == 0 or row == 4) and (col > 0 and col < 4)
                ):
                    sel_eye += 1
                    portalframe += eyes[sel_eye - 1]
                elif (col != 0 or col != 4) and (col > 0 and col < 4):
                    portalframe += "{end_portal}" if eye_count >= 12 else "{lava}"
                else:
                    portalframe += "{air}"
            portalframe += "\n"

        # replace placeholder with portal frame emoji
        for placeholder in emojis.keys():
            portalframe = portalframe.replace(placeholder, emojis[placeholder])

        e = discord.Embed(
            title="findseed but pipega",
            description=f"Your seed is a **{eye_count}** eye: \n\n{portalframe}",
            color=discord.Colour(0x38665E),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.reply(embed=e)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["dl"])
    async def dreamluck(self, ctx):
        """`Test your Minecraft RNG, but in a bot command`"""
        blaze = sum([1 for i in range(306) if random() * 100 <= 50])

        pearl = sum([1 for i in range(263) if random() <= (20 / 473)])

        e = discord.Embed(
            title=f"Your Pearl Trades -> {pearl}/262",
            description="While Dream's luck was -> 42/262",
            colour=discord.Colour(0x08443A),
        )
        a = discord.Embed(
            title=f"Your Blaze Drops -> {blaze}/305",
            description="While Dream's luck was 211/305",
            colour=discord.Colour.gold(),
        )
        await ctx.reply(embed=e)
        await ctx.send(embed=a)

    @commands.command()
    async def flip(self, ctx):
        """`Flip a coin, thats it`"""
        await ctx.reply(f"You got {choice(['heads', 'tails'])}!")

    @commands.command(
        usage="(choice)",
        brief="`The Classic Paper Rock Sccicors game, but with no friends, instead its with the bot`",
        example="{prefix}rps rock",
    )
    async def rps(self, ctx, choice: str):
        """`Play Rock Paper Sccisors with the bot`"""
        choice = choice.lower()
        rps = ["rock", "paper", "scissors"]
        bot_choice = rps[randint(0, len(rps) - 1)]

        await ctx.reply(
            f"You chose ***{choice.capitalize()}***."
            + f" I chose ***{bot_choice.capitalize()}***."
        )
        if bot_choice == choice:
            await ctx.reply("It's a Tie!")
        elif bot_choice == rps[0]:

            def f(x):
                return {"paper": "Paper wins!", "scissors": "Rock wins!"}.get(
                    x, "Rock wins!"
                )

            result = f(choice)
        elif bot_choice == rps[1]:

            def f(x):
                return {"rock": "Paper wins!", "scissors": "Scissors wins!"}.get(
                    x, "Paper wins!"
                )

            result = f(choice)
        elif bot_choice == rps[2]:

            def f(x):
                return {"paper": "Scissors wins!", "rock": "Rock wins!"}.get(
                    x, "Scissors wins!"
                )

            result = f(choice)
        else:
            return
        if choice == "noob":
            result = "Noob wins!"
        await ctx.reply(result)

    @commands.command()
    async def findsleep(self, ctx):
        """`See how long you sleep, this is 100% true I swear`"""

        lessSleepMsg = [
            "gn, insomniac!",
            "counting sheep didn't work? try counting chloroform vials!",
            "try a glass of water",
            "some decaf coffee might do the trick!",
        ]

        moreSleepMsg = [
            "waaakeee uuuppp!",
            "are they dead or asleep? I can't tell.",
            "wake up, muffin head",
            "psst... coffeeee \\:D",
        ]

        sleepHrs = randint(0, 24)

        if sleepHrs == 0:
            await ctx.reply(
                f"{ctx.author.mention} -> your sleep is 0 hours long - nice try :D"
            )
        elif sleepHrs <= 5:
            if sleepHrs == 1:
                s = ""
            else:
                s = "s"
            await ctx.reply(
                f"{ctx.author.mention} -> your sleep is {sleepHrs} hour{s} long - {lessSleepMsg[randint(0, len(lessSleepMsg) - 1)]}"
            )
        else:
            await ctx.reply(
                f"{ctx.author.mention} -> your sleep is {sleepHrs} hours long - {moreSleepMsg[randint(0, len(moreSleepMsg) - 1)]}"
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if message.author.bot:
            return
        if (
            "<@!821142944077447228>" in message.content
            or "<@821142944077447228>" in message.content
        ):
            await message.channel.send("<​:ping:856592070969262163>")

        if message.author.bot:
            return

        bad_words = ["fair", "ⓕⓐⓘⓡ", "ɹıɐɟ", "justo", "adil"]
        fair = ""
        for word in bad_words:
            if word in message.content.lower().replace(" ", ""):
                fair += f"{word.title()} "
        if fair:
            try:
                await message.channel.send(fair)
            except UnboundLocalError:
                pass

    @commands.command()
    async def e(self, ctx):
        """`If you say e, I say e, yes`"""
        await ctx.reply('e')

    @commands.cooldown(5, 10, type=commands.BucketType.user)
    @commands.command(aliases=["piglin"], usage="[amount of gold]", example="{prefix}barter 64")
    async def barter(self, ctx, gold: int = 64):
        """`Barter with Minecraft's Piglin. (Based on JE 1.16.1, before nerf)`"""
        # limit gold amount up to 2240 (Minecraft inventory limit)
        if gold > 2240:
            gold = 2240
        if gold <= 0:
            gold = 1

        trade = Piglin(gold)

        items = {}
        for item in trade.items:
            try:
                items[item.name][1] += item.quantity
            except KeyError:
                items[item.name] = [item.id, item.quantity]

        def emoji(name: str):
            return {
                "enchanted-book": "<:enchanted_book:807319425848967258>",
                "iron-boots": "<:enchanted_iron_boots:807319425711210528>",
                "iron-nugget": "<:iron_nuggets:807318404364107776>",
                "splash-potion-fire-res": "<:splashpotionoffireres:807318404024762409>",
                "potion-fire-res": "<:potionoffireres:807318404355719188>",
                "quartz": "<:quartz:807318404285333514>",
                "glowstone-dust": "<:glowstonedust:807318404431085587>",
                "magma-cream": "<:magma_cream:807318404393599046>",
                "ender-pearl": "<:enderpearls:807318454751068180>",
                "string": "<:string:807318404091740216>",
                "fire-charge": "<:fire_charge:807318403894607913>",
                "gravel": "<:garvel:807318404347330610>",
                "leather": "<:leather:807318404385341520>",
                "nether-brick": "<:nether_bricks:807318404020043797>",
                "obsidian": "<:obsidian:807318404318363658>",
                "cry-obsidian": "<:crying_obsidian:807318454423650305>",
                "soul-sand": "<:soul_sand:807318404297785364>",
            }.get(name, "❔")

        e = discord.Embed(
            title="Bartering with {} gold{}  <a:loading:854498073416695849>".format(gold, "s" if gold > 1 else ""),
            colour=discord.Colour.gold()
        )
        e.set_author(
            name=f"{ctx.message.author}",
            icon_url=ctx.message.author.avatar_url,
        )
        a = discord.Embed(
            title="Bartering with {} gold{}".format(gold, "s" if gold > 1 else ""),
            description="You got:\n\n{}".format(
                "\n".join(["{} → {}".format(
                    emoji(v[0]), v[1]) for v in items.values()]
                )
            ),
            colour=discord.Colour.gold(),
        )
        a.set_author(
            name=f"{ctx.message.author}",
            icon_url=ctx.message.author.avatar_url,
        )
        message = await ctx.reply(embed=e)
        await asyncio.sleep(5)
        await message.edit(embed=a)

    @commands.command()
    async def joke(self, ctx):
        """`Ask the bot a joke and he will tell you a joke that will defenetly make you laugh no cap`"""
        data = requests.get('https://official-joke-api.appspot.com/jokes/random').json()
        embed = discord.Embed(title=data['setup'], description=data['punchline'], color=0xf4565a)
        await ctx.reply(embed=embed)

    @commands.command()
    async def joemama(self, ctx):
        """`Ask the bot a Yo Mama Joke, he will diliver`"""
        embed = discord.Embed(title=f'{getyomum()}', color=0xf4565a)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['saysomethingniceto'])
    async def compliment(self, ctx, member: discord.Member = None):
        """`Compliment Someone :D`"""

        if member is None:
            member = choice([member for member in ctx.guild.members if not member.bot])
            e = discord.Embed(
                colour=discord.Color(0x2EDC8A),
                title=f'{getcompliment()}',
            )

            await ctx.reply(content=f"{member.mention}", embed=e)
            return

        else:
            NO = discord.AllowedMentions(
                users=False,
            )
            e = discord.Embed(
                colour=discord.Color(0x2EDC8A),
                title=f'{getcompliment()}',
            )

            await ctx.reply(content=f"{member.mention}", allowed_mentions=NO, embed=e)
            return

    @commands.command(aliases=['guess', 'gtn', 'guessnum'])
    async def guessthenumber(self, ctx):
        """`Guess the number, why did you even do help guess if its self explanitory`"""
        number = randint(1, 100)
        guess = False
        for i in range(1, 86):
            if i == 11:
                await ctx.reply("The game is over and you lost.")
                return
            await ctx.reply(f'Guess the number! Pick from 1 to 100 and get some hints! This is attempt #{i}.')
            response = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            try:
                guess = int(response.content)
            except ValueError:
                await ctx.reply("That was not a number. Systems failing..... game aborted")
                break
            if guess > number:
                await ctx.reply('The number is smaller than that.')
            elif guess < number:
                await ctx.reply('The number is bigger than that')
            else:
                await ctx.reply(f'You got it! It took you {i} attempts.')
                guess = True
                break
        if not guess:
            await ctx.reply(f"The number was {number}, too bad.")

    @commands.command(aliases=['random'])
    async def rng(self, ctx, minimum: int, maximum: int):
        """`Choose a minimum and a maximum number and the bot will choose a random number`"""
        await ctx.reply(randint(minimum, maximum))

    @commands.command()
    async def roll(self, ctx, pool):
        """`Roll the dice`"""
        await ctx.reply(f"You rolled a {randint(0, int(pool))}")

    @commands.command(aliases=["8ball"])
    async def ballofwisdom(self, ctx, *, question):
        """`Ask the Magic 8Ball your question,a nd he will answer correctly no cap`"""
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        e = discord.Embed(
            title=f"🎱  {question}?",
            colour=discord.Colour(0x603593),
            description=choice(responses),
            )

        await ctx.reply(embed=e)

    @commands.command(aliases=["isimposter"], usage="[impostor count] [player count]")
    async def isimpostor(self, ctx, impostor: int = 1, player: int = 10):
        """`Check if you're an impostor or a crewmate.`"""
        if 3 < impostor < 1:
            await ctx.reply("Impostor counter can only be up to 3 impostors")
            return
        chance = 100 * impostor / player / 100
        if random() < chance:
            await ctx.reply(f"{ctx.author.mention}, you're a crewmate!")
        else:
            await ctx.reply(f"{ctx.author.mention}, you're an impostor!")

    @commands.command()
    async def roast(self, ctx, member: discord.Member = None):
        """`Roast someone >:)`"""

        no_roast = {
            783159643126890517,
        }

        if member is None:
            member = choice([member for member in ctx.guild.members if not member.bot])
            e = discord.Embed(
                colour=discord.Color(0xE41919),
                title=f'{getroast()}',
            )

            await ctx.reply(content=f"{member.mention}", embed=e)
            return

        if member.id in no_roast:
            a = discord.Embed(
                colour=discord.Color(0xE41919),
                title="Im not roasting my self you dum dum.",
            )

            await ctx.reply(embed=a)
            return

        else:
            NO = discord.AllowedMentions(
                users=False,
            )
            e = discord.Embed(
                colour=discord.Color(0xE41919),
                title=f'{getroast()}',
            )

            await ctx.reply(content=f"{member.mention}", allowed_mentions=NO, embed=e)
            return

    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def someone(self, ctx):
        """`Discord's mistake`"""
        await ctx.reply(choice([member for member in ctx.guild.members if not member.bot]).mention)

    @commands.command()
    async def findtaxes(self, ctx):
        """`See how much you owe in taxes`"""

        lessTaxesMsg = [
            "You really do pay your taxes",
            "How do you do this",
            "Do you do manual maths?",
            "Im amazed",
        ]

        moreTaxesMsg = [
            "How many years have you gone without paying taxes",
            "How come the IRS has not taken your house",
            "How the hell do you owe so much",
            "The IRS is having a lot of patience on ya",
        ]

        taxmona = randint(0, 1000000)

        if taxmona == 0:
            await ctx.reply(
                f"{ctx.author.mention} -> You owe nothing, are you 65 years old?"
            )
        elif taxmona <= 5000:
            if taxmona == 1:
                s = ""
            else:
                s = "s"
            await ctx.reply(
                f"{ctx.author.mention} -> you owe ${taxmona} dollar{s} - {lessTaxesMsg[randint(0, len(lessTaxesMsg) - 1)]}"
            )
        else:
            await ctx.reply(
                f"{ctx.author.mention} -> you owe ${taxmona} in taxes - {moreTaxesMsg[randint(0, len(moreTaxesMsg) - 1)]}"
            )

    @commands.group(aliases=['bb'], example=["group"], invoke_without_command=True)
    async def blackboxgame(self, ctx, arg=None):
        """`A little game I created`"""
        emojis = {
            "{bad}": "<:cross:854498023061061633>",
            "{good}": "<:check:854498005221769228>"
        }

        # range(25) for 7x7
        goodBad = ["||{bad}||" if randint(1, 5) == 1 else "||{good}||" for i in range(49)]

        output = ""
        stuff = 0
        for row in range(7):
            for col in range(7):
                output += goodBad[stuff]
                stuff += 1
            output += "\n"

        for e in emojis.keys():
            output = output.replace(e, emojis[e])

        e = discord.Embed(
            title="The Black Box Game!",
            description=f"{output}",
            color=discord.Colour(0xE41919),
            )
        e.set_footer(
            text="Do -bb htp to learn how to play the game!"
        )

        await ctx.reply(embed=e)

    @blackboxgame.command(name="htp")
    async def htp(self, ctx):
        htp = discord.Embed(
            colour=discord.Color(0xE41919),
            title="**How to Play The Black Box**",
            description="In this game, you are going to press the black boxes, you are going to try and get as many <:check:854498005221769228> as you can.\n"
            + "If you get a <:cross:854498023061061633>, you lose.\n"
            + "Every box has a 15% chance of being an <:cross:854498023061061633>\n"
            + "GL! If you want to play do `-bb` to start playing",
        )
        await ctx.reply(embed=htp)

    @commands.command()
    async def findseeds(self, ctx, attempts: int = 100):
        """`Findseed, but you can do multiple in one`"""
        if attempts > 100000:
            attempts = 100000
        if attempts <= 0:
            await ctx.reply("Give the amout of seeds you want to findseeds")
            return
        if attempts == 1:
            await ctx.reply("You know that `-findseed` exists, right?")
            return

        eyes = {}
        for i in range(attempts):
            curEye = sum([1 for i in range(12) if randint(1, 10) == 1])
            try:
                eyes[curEye] += 1
            except KeyError:
                eyes[curEye] = 1

        e = discord.Embed(
            title=f"This is what you got in {attempts} seeds",
            description="\n".join(["**{}** eyes: `{}` seeds".format(k, v) for k, v in sorted(eyes.items())]),
            color=discord.Colour(0x349988),
        )
        e.set_author(
            name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.reply(embed=e)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        """`Offer a hug to someone.`"""
        e = discord.Embed(
            title="{} offered you a hug!".format(ctx.author.display_name),
            description="React to the emoji below to accept!",
            color=discord.Colour(0x000000)
        )
        NO = discord.AllowedMentions(
            users=False,
        )
        e.set_footer(text="Waiting for answer...", icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(content=f"{member.mention} {ctx.author.mention}", allowed_mentions=NO, embed=e)
        await msg.add_reaction("<:hug:855154433864630272>")

        def check(reaction, reactor):
            # return true or false, if its true the action continue
            return (reactor == member and str(reaction.emoji) == "<:hug:855154433864630272>")

        try:
            # waiting for "true"
            reaction, reactor = await self.bot.wait_for("reaction_add", timeout=120.0, check=check)
        except asyncio.TimeoutError:
            e.set_footer(
                text="Offer has been declined.", icon_url=ctx.author.avatar_url
            )
            await msg.edit(embed=e)
            await msg.clear_reactions()
        else:
            # hug go brrrr
            e.set_footer(
                text="Offer has been accepted!", icon_url=ctx.author.avatar_url
            )
            await msg.edit(embed=e)
            e = discord.Embed(
                title="{} hugged {}!".format(ctx.author.display_name, member.display_name),
                color=discord.Colour(0x000000)
            )
            e.set_image(
                url="https://cdn.discordapp.com/attachments/745481731582197780/845473845598224384/hugging.png"
            )
            await ctx.send(content=f"{member.mention} {ctx.author.mention}", embed=e)

    @commands.command()
    async def hack(self, ctx, member: discord.Member = None):
        """`Hack someone >:D`"""

        if member is None:
            await ctx.reply("Give me a Member to hack")
            return

        hack = await ctx.reply(
            "<a:loading:854498073416695849> | Booting up Hacking Program..."
        )
        await asyncio.sleep(3)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<a:loading:854498073416695849> | Hacking {member}'s' IP-Address..."
        )
        await asyncio.sleep(3)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<a:loading:854498073416695849> | Locating {member}'s Address..."
        )
        await asyncio.sleep(3)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<a:loading:854498073416695849> | Hacking {member}'s Devices..."
        )
        await asyncio.sleep(3)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
            f"<a:loading:854498073416695849> | Scanning {member}'s Files..."
        )
        await asyncio.sleep(3)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Files!\n"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Files!\n"
            "<a:loading:854498073416695849> | Gathering Information..."
        )

        messages = []
        url = []
        for channel in ctx.guild.text_channels:
            async for message in channel.history(limit=500):
                if message.author == member and message.attachments:
                    messages += [message]
                    url += [att.url for att in message.attachments]

        if not url:
            url = []
            url = [
                "https://cdn.discordapp.com/attachments/745481731582197780/855624001652260894/hack1.png",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624003376775195/hack2.jpeg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624004979261450/hack3.jpg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624007943454720/hack4.jpg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624048749838376/hack5.jpg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624050177081394/hack6.jpg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624052235042856/hack7.jpg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624054459072512/hack8.jpeg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624056157241374/hack9.jpeg",
                "https://cdn.discordapp.com/attachments/745481731582197780/855624083685376010/hack10.jpeg",
            ]

        embed = discord.Embed(
            title=""
        )
        embed.set_image(
            url=f"{choice(url)}"
        )

        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Files!\n"
            "<:completed:854498023291092992> | Completed!"
        )
        await asyncio.sleep(1)
        await hack.edit(
            content="<:completed:854498023291092992> | Hacking Program booted!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s IP-Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Address!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Devices!\n"
            f"<:completed:854498023291092992> | Hacked {member}'s Files!\n"
            "<:completed:854498023291092992> | Completed!\n"
            "\n"
            "Here's what I found:", embed=embed
        )

    @commands.command()
    async def snipe(self, ctx):
        """`Snipe a message`"""
        channel = ctx.channel
        try:
            snipeEmbed = discord.Embed(
                title="",
                description=self.snipe_message[channel.id].content,
                color=discord.Colour(0x000000)
                )
            snipeEmbed.set_author(
                name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
                icon_url=ctx.message.author.avatar_url,
            )
            await ctx.reply(embed=snipeEmbed)
        except AttributeError:
            await ctx.reply("There is nothing to snipe!")

    @commands.command()
    async def quote(self, ctx):
        """`Ask the bot for an inspirational quote`"""
        data = requests.get('https://api.quotable.io/random').json()
        embed = discord.Embed(
            title=data['content'],
            description=f"- {data['author']}",
            color=0x4EB9FE
            )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["say"], hidden=True)
    @checks.is_botmaster()
    async def phrase(self, ctx, *, phrase):
        """`Tell the bot what to say!`"""
        await discord.Message.delete(ctx.message)
        await ctx.send(f'{phrase}')


def setup(bot):
    bot.add_cog(Fun(bot))
