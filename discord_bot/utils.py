import discord
import d20

async def try_delete(message):
    try:
        await message.delete()
    except discord.HTTPException:
        pass

def get_version():
    with open('./version.txt') as f:
        text = f.read()
        print(f"build version {text}")
        return text

class VerboseMDStringifier(d20.MarkdownStringifier):
    def _str_expression(self, node):
        return f"**{node.comment or 'Result'}**: {self._stringify(node.roll)}\n**Total**: {int(node.total)}"

class BladesStringifier(d20.MarkdownStringifier):
    def _str_expression(self, node):
        #determine if this is zero-dice roll
        operation = node.children[0].operations[0]
        if operation.op=="k":
            normal_roll=True
        else:
            normal_roll=False
        if normal_roll:
            die_value = 0
        else:
            die_value = 7
        critical = False
        for child in node.children[0].values:
            if normal_roll:
                if child.values[0].total >= die_value:
                    if die_value == 6 and child.values[0].total == 6:
                        critical = True
                    die_value = child.values[0].total
            else: #low roll
                if child.values[0].total <= die_value:
                    die_value = child.values[0].total
        if critical:
            resulttype = "Critical Success!"
        elif die_value == 6:
            resulttype = "Full Success!"
        elif die_value > 3:
            resulttype = "Partial Success"
        else:
            resulttype = "Bad Outcome"
        #TODO: remove dice pattern from stringify below
        return f"**Dice**: {self._stringify(node.roll)}\n**Result**: {resulttype}"

    def _str_dice(self, node):
        the_dice = [self._stringify(die) for die in node.values]
        return f"({', '.join(the_dice)})"


class PersistentRollContext(d20.RollContext):
    """
    A roll context that tracks lifetime rolls as well as individual rolls.
    """

    def __init__(self, max_rolls=1000, max_total_rolls=None):
        """
        :param max_rolls: The maximum number of rolls allowed in an individual roll.
        :param max_total_rolls: The maximum number of rolls allowed throughout this object's lifetime.
        """
        super().__init__(max_rolls)
        self.max_total_rolls = max_total_rolls or max_rolls
        self.total_rolls = 0

    def count_roll(self, n=1):
        super().count_roll(n)
        self.total_rolls += 1
        if self.total_rolls > self.max_total_rolls:
            raise d20.TooManyRolls("Too many dice rolled.")