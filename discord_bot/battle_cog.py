from discord.ext import commands
import tracker


class BattleTracker(commands.Cog):

    channel_battledata = {}
    user_last_reg = {}
    channel_last_post = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx, name: str, maxhp: int, *args):
        curhp = maxhp
        flags = tracker.CombatantFlags()
        for arg in args:
            print(f"\t {arg}")
            try:
                curhp = int(arg)
            except ValueError:
                pass
            flags.set_flag(arg)
        combatant = tracker.BattleCombatant(name, maxhp, curhp, flags)
        data = self.get_data(ctx.channel.id)
        data.add_combatant(combatant)
        self.user_last_reg[ctx.author.id] = name
        print(data)
        await ctx.send(f"Registered combatant {name}!")

    @commands.command()
    async def setstatus(self, ctx, status: str, *args):
        names = []
        if len(args) > 0:
            names.extend(args)
        else:
            names.append(self.user_last_reg[ctx.author.id])
        data = self.get_data(ctx.channel.id)
        print(names)
        for name in names:
            combatant = data.get_combatant(name)
            print("look for {combatant}")
            print(f"in {data.combatants.keys()}")
            if combatant:
                combatant.status = status

    @commands.command()
    async def clearstatus(self, ctx, *args):
        await self.setstatus(ctx, "", *args)

    @commands.command()
    async def reggroup(self, ctx, name: str, number: int, maxhp: int, *args):
        curhp = maxhp
        flags = tracker.CombatantFlags()
        for arg in args:
            print(f"\t {arg}")
            try:
                curhp = int(arg)
            except ValueError:
                pass
            flags.set_flag(arg)
        data = self.get_data(ctx.channel.id)
        for i in range(number):
            combatant = tracker.BattleCombatant(name + f'-{i+1}', maxhp, curhp, flags)
            data.add_combatant(combatant)
        await ctx.send(f"Registered {number} combatants with name prefix {name}!")

    @commands.command()
    async def initgroup(self, ctx, score: int, nameprefix: str):
        data = self.get_data(ctx.channel.id)
        names = data.get_names_with_prefix(nameprefix)
        await self.init(ctx, score, *names)

    @commands.command()
    async def cleanup(self, ctx):
        async for message in ctx.channel.history(limit=200):
            if message.author == ctx.bot.user:
                try:
                    await message.delete()
                except Exception:
                    pass

    @commands.command()
    async def remove(self, ctx, name: str):
        removed = self.get_data(ctx.channel.id).remove_combatant(name)
        if removed:
            await ctx.send(f"Removed combatant {name} from tracker.")
        else:
            await ctx.send(f"No combatant with name {name} to remove.")

    @commands.command()
    async def start(self, ctx):
        self.get_data(ctx.channel.id).combat_active = True
        await ctx.send("Starting Combat!")

    @commands.command()
    async def stop(self, ctx):
        self.get_data(ctx.channel.id).combat_active = False
        await ctx.send("End Combat")

    @commands.command()
    async def init(self, ctx, score: int, *args):
        data = self.get_data(ctx.channel.id)
        print(args)
        if len(args) > 0:
            set_combatants = []
            fail_combatants = 0
            for name in args:
                print(f"setting for name {name}")
                combatant = data.set_initiative(name, score)
                if combatant:
                    set_combatants.append(combatant.name)
                else:
                    fail_combatants = fail_combatants + 1
            if len(set_combatants) > 0:
                await ctx.send(f"Set initiative for combatant{'s' if len(set_combatants) > 1 else ''} {', '.join(set_combatants)} to {score}")
            if fail_combatants > 0:
                await ctx.send(f"failed setting initiative for {fail_combatants} provided names.")
        elif ctx.author.id in self.user_last_reg:
            name = self.user_last_reg[ctx.author.id]
            combatant = data.set_initiative(name, score)
            if combatant:
                await ctx.send(f"Set initiative score for {name}{'' if combatant.flags.hide_name else f' to {score}'}")
            else:
                await ctx.send("Last registered combatant has been removed from the combat, and no name provided.  Not setting initiative.")
        else:
            await ctx.send(f"No combatant registered for user {ctx.author.name}, and none provided.  Not setting initiative.")

    async def cog_after_invoke(self, ctx):
        await ctx.message.delete(delay=5)
        data = self.get_data(ctx.channel.id)
        if data.combat_active:
            await self.print_combat(ctx, data)

    async def print_combat(self, ctx, combatdata):
        lastmessage = self.channel_last_post.get(ctx.channel.id, None)
        message = await ctx.send(str(combatdata))
        if message:
            self.channel_last_post[ctx.channel.id] = message
        if lastmessage:
            await lastmessage.delete()

    def get_data(self, serverid):
        if serverid in self.channel_battledata:
            return self.channel_battledata[serverid]
        else:
            data = tracker.BattleData()
            self.channel_battledata[serverid] = data
            return data
