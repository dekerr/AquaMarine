from discord.ext import commands, vbu

from cogs import utils


class Upgrades(vbu.Cog):

    UPGRADE_DESCRIPTIONS = {
        "rod_upgrade": "Increases the price a caught fish sells for",
        "line_upgrade": "Increases the chance of catching two fish in one cast",
        "crate_chance_upgrade": "Increases chance of catching a crate when fishing",
        "weight_upgrade": "Increases the level fish are when caught",
        "bait_upgrade": "Increases the chance of catching rarer fish when fishing",
        "crate_tier_upgrade": "Increases the tier of the crate caught",
        "lure_upgrade": "Increases the chance of catching a special fish when fishing",
        "feeding_upgrade": "Increases how long fish will live after being fed",
        "toys_upgrade": "Increases the xp gained from entertaining",
        "mutation_upgrade": "Increases the chance of a fish mutating to a special fish during cleaning",
        "amazement_upgrade": "Increases chance of bonus level when entertaining",
        "bleach_upgrade": "Increases the cleaning multiplier",
        "big_servings_upgrade": "Increases chance of a fish not eating food when they are fed",
        "hygienic_upgrade": "Lessens the frequency of cleaning, while giving a multiplier equal to the lost time",
    }

    # TIER 3
    BAIT_UPGRADES = ["line_upgrade", "lure_upgrade"]
    CRATE_CHANCE_UPGRADES = ["weight_upgrade", "crate_tier_upgrade"]
    TOYS_UPGRADES = ["amazement_upgrade", "mutation_upgrade"]
    BIG_SERVINGS_UPGRADES = ["hygienic_upgrade", "feeding_upgrade"]

    # TIER 2
    ROD_UPGRADES = {
        "bait_upgrade": BAIT_UPGRADES,
        "crate_chance_upgrade": CRATE_CHANCE_UPGRADES,
    }
    BLEACH_UPGRADES = {
        "toys_upgrade": TOYS_UPGRADES,
        "big_servings_upgrade": BIG_SERVINGS_UPGRADES,
    }

    # TIER 1
    TIER_RANKS = {
        "rod_upgrade": ROD_UPGRADES,
        "bleach_upgrade": BLEACH_UPGRADES,
    }

    UPGRADE_COST_LIST = (1000, 2000, 3000, 4000, 5000, 5000)
    UPGRADE_COST_LIST_TWO = (10000, 20000, 30000, 40000, 50000, 50000)
    UPGRADE_COST_LIST_THREE = (100000, 200000, 300000, 400000, 500000, 500000)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def upgrades(self, ctx: commands.Context):
        """
        Show you your upgrades and the price of the next level.
        """

        # The output that we want to build
        message = []  # A list of text to send
        emote_string_list = []  # Their emoji progress bar

        # Grab their upgrades from the database
        async with vbu.Database() as db:
            upgrades = await db(
                """SELECT rod_upgrade, bait_upgrade, line_upgrade, lure_upgrade, crate_chance_upgrade, weight_upgrade,
                crate_tier_upgrade, bleach_upgrade, toys_upgrade, amazement_upgrade, mutation_upgrade,
                big_servings_upgrade, hygienic_upgrade, feeding_upgrade
                FROM user_upgrades WHERE user_id = $1""",
                ctx.author.id,
            )
            if not upgrades:
                upgrades = await db(
                    """INSERT INTO user_upgrades (user_id) VALUES ($1) RETURNING *""",
                    ctx.author.id,
                )

        # Build out output strings
        tier = 0
        tree_number = 0
        fields = []
        for upgrade, level in upgrades[0].items():
            if upgrade != "user_id":
                tier += 1
                description = self.UPGRADE_DESCRIPTIONS[upgrade]
                name = " ".join(upgrade.split("_")).title()
                # Get the cost of an upgrade
                cost_string = f"{self.UPGRADE_COST_LIST[int(level)]:,} <:sand_dollar:877646167494762586>"

                if tier == 1:
                    parent_one = upgrade

                left_bar = "<:bar_L:886377903615528971>"
                start = ""
                start_two = ""
                emote = "<:bar_1:877646167184408617>"
                if tier == 2 or tier == 5:
                    cost_string = f"{self.UPGRADE_COST_LIST_TWO[int(level)]:,} <:sand_dollar:877646167494762586>"
                    parent_two = upgrade
                    if upgrades[0][parent_one] != 5:
                        description = "???"
                        name = "???"
                        cost_string = "???"
                    start = "<:straight_branch:886377903837806602>"
                    start_two = "<:straight:886377903879753728>"
                    emote = "<:bar_2:877646166823694437>"
                    left_bar = "<:bar_L_branch:886377903581986848>"
                    if tier == 5:
                        start = "<:branch:886377903825252402>"
                        start_two = "<:straight:886377903879753728>"
                elif tier == 6 or tier == 3:
                    cost_string = f"{self.UPGRADE_COST_LIST_THREE[int(level)]:,} <:sand_dollar:877646167494762586>"
                    if upgrades[0][parent_two] != 5:
                        description = "???"
                        name = "???"
                        cost_string = "???"
                    start = "<:__:886381017051586580><:straight_branch:886377903837806602>"
                    emote = "<:bar_3:877646167138267216>"
                    left_bar = "<:bar_L_straight:886379040884260884>"
                    if tier == 3:
                        start_two = "<:straight:886377903879753728><:straight:886377903879753728>"
                        start = "<:straight:886377903879753728><:straight_branch:886377903837806602>"
                    else:
                        start_two = "<:__:886381017051586580><:straight:886377903879753728>"
                elif tier == 4 or tier == 7:
                    cost_string = f"{self.UPGRADE_COST_LIST_THREE[int(level)]:,} <:sand_dollar:877646167494762586>"
                    if upgrades[0][parent_two] != 5:
                        description = "???"
                        name = "???"
                        cost_string = "???"
                    emote = "<:bar_3:877646167138267216>"
                    left_bar = "<:bar_L_straight:886379040884260884>"
                    if tier == 4:
                        start_two = "<:straight:886377903879753728><:straight:886377903879753728>"
                        start = "<:straight:886377903879753728><:branch:886377903825252402>"
                    else:
                        start_two = "<:__:886381017051586580><:straight:886377903879753728>"
                        start = "<:__:886381017051586580><:branch:886377903825252402>"
                # If they're fully upgraded
                if level == 5:
                    cost_string = "This Upgrade is fully upgraded."

                # Each level they have is a full bar emoji, up to 5 characters long
                emote_string_list.clear()  # Clear our emoji list first
                for _ in range(level):

                    emote_string_list.append(emote)

                while len(emote_string_list) < 5:
                    emote_string_list.append("<:bar_e:877646167146643556>")
                print(emote_string_list)

                # Generate the message to send

                progress_bar = f"{left_bar}{''.join(emote_string_list)}<:bar_R:877646167113080842>"
                nl = "\n"
                message.append(
                    (
                        f"{start}{progress_bar}",
                        f"{start_two}**{name}: (Lvl. {level}.): {cost_string}**{nl}{start_two}*{description}*",
                    )
                )
                print(len(progress_bar))

                if tier == 7:
                    message.append(("** **", "** **"))
                    tree_number += 1
                    tier = 0

        # And send our message
        embed = vbu.Embed()
        for time, message_data in enumerate(message):
            if time == 0:
                embed.add_field(
                    name="The Way of the Fish",
                    value="These upgrades have to do with fishing",
                    inline=False,
                )
            elif time == 8:
                embed.add_field(
                    name="The Way of the Tank",
                    value="These upgrades have to do with owning fish in aquariums",
                    inline=False,
                )
            embed.add_field(
                name=message_data[1], value=message_data[0], inline=False
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def upgrade(self, ctx: commands.Context, *, upgrade: str):
        """
        Upgrade one of your items.
        """

        # Grab the user's current upgrades
        async with vbu.Database() as db:
            upgrades = await db(
                """SELECT rod_upgrade, line_upgrade, crate_chance_upgrade,
                weight_upgrade, bait_upgrade, crate_tier_upgrade,
                lure_upgrade, feeding_upgrade, toys_upgrade,
                mutation_upgrade, amazement_upgrade, bleach_upgrade,
                big_servings_upgrade, hygienic_upgrade
                FROM user_upgrades WHERE user_id = $1""",
                ctx.author.id,
            )

        upgrades = upgrades[0]

        upgrade_base_name = upgrade.lower().removesuffix(" upgrade")
        upgrade = upgrade_base_name.replace(" ", "_") + "_upgrade"

        max_level = 5

        def fully_leveled(item):
            return item == max_level

        def upgrade_error(msg_text):
            msg_text = msg_text.replace("_", " ").title()
            error_msg = f"The {msg_text} needs upgraded first!"
            return error_msg

        # Check tier 3 dependencies
        if upgrade in self.BAIT_UPGRADES:
            if not fully_leveled(upgrades["bait_upgrade"]):
                return await ctx.send(upgrade_error("bait_upgrade"))
        elif upgrade in self.CRATE_CHANCE_UPGRADES:
            if not fully_leveled(upgrades["crate_chance_upgrade"]):
                return await ctx.send(upgrade_error("crate_chance_upgrade"))
        elif upgrade in self.TOYS_UPGRADES:
            if not fully_leveled(upgrades["toys_upgrade"]):
                return await ctx.send(upgrade_error("toys_upgrade"))
        elif upgrade in self.BIG_SERVINGS_UPGRADES:
            if not fully_leveled(upgrades["big_servings_upgrade"]):
                return await ctx.send(upgrade_error("big_servings_upgrade"))

        # Check tier 2 dependencies
        elif upgrade in self.ROD_UPGRADES:
            if not fully_leveled(upgrades["rod_upgrade"]):
                return await ctx.send(upgrade_error("rod_upgrade"))
        elif upgrade in self.BLEACH_UPGRADES:
            if not fully_leveled(upgrades["bleach_upgrade"]):
                return await ctx.send(upgrade_error("bleach_upgrade"))
        else:
            return await ctx.send("That's not a valid upgrade.")

        # See how upgraded the user currently is
        upgrade_level = upgrades[upgrade]
        if fully_leveled(upgrade_level):
            return await ctx.send("That upgrade is fully upgraded.")

        # Calculate cost based on upgrade tier
        tier_two_upgrades = set().union(*self.TIER_RANKS.values())
        if upgrade in self.TIER_RANKS:
            upgrade_cost_list_used = self.UPGRADE_COST_LIST
        elif upgrade in tier_two_upgrades:
            upgrade_cost_list_used = self.UPGRADE_COST_LIST_TWO
        else:
            upgrade_cost_list_used = self.UPGRADE_COST_LIST_THREE

        if not await utils.check_price(
            self.bot,
            ctx.author.id,
            upgrade_cost_list_used[int(upgrade_level)],
            "balance",
        ):
            return await ctx.send(
                "You don't have enough Sand Dollars <:sand_dollar:877646167494762586> for this upgrade!"
            )

        # Upgrade them in the database
        async with vbu.Database() as db:
            await db(
                """UPDATE user_balance SET balance=balance-$1 WHERE user_id = $2""",
                upgrade_cost_list_used[int(upgrades[upgrade])],
                ctx.author.id,
            )
            await db(
                f"""UPDATE user_upgrades SET {upgrade}=user_upgrades.{upgrade}+1 WHERE user_id = $1""",
                ctx.author.id,
            )

        # And bam
        await ctx.send(
            f"You bought the Level {upgrade_level + 1} "
            f"{upgrade_base_name.title()} Upgrade for "
            f"{upgrade_cost_list_used[upgrade_level]:,}!"
        )


def setup(bot):
    """Bot Setup"""
    bot.add_cog(Upgrades(bot))
