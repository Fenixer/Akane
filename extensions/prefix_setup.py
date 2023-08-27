import typing as t

import hikari as hk
import lightbulb as lb

from functions.utils import humanized_list_join

prefix_manager = lb.Plugin("Prefix", "manager", include_datastore=True)
prefix_manager.d.help = True


@prefix_manager.command
@lb.command("prefix", "Prefix manager wizard", aliases=["pfx"])
@lb.implements(lb.PrefixCommandGroup)
async def prefix_group(ctx: lb.PrefixContext) -> None:
    if len(ctx.event.message.split()) == 1:
        await ctx.respond("These are your prefixes")
    else:
        pass


@prefix_group.child
@lb.add_checks(lb.owner_only | lb.has_guild_permissions(hk.Permissions.ADMINISTRATOR))
@lb.option(
    "prefixes",
    "The prefix to add (guild specific)",
    modifier=lb.OptionModifier.GREEDY,
)
@lb.command("add", "Add prefix(es)", aliases=["a"], pass_options=True)
@lb.implements(lb.PrefixSubCommand)
async def add_prefix(ctx: lb.Context, prefixes: t.Sequence[str]) -> None:
    # prefixes = prefixes.split()
    if len(prefixes) > 3:
        await ctx.respond("Can only have upto 3 guild prefixes")
        return
    # Enforce prefix length to be upto 5 charas
    # If same as global, then enable global/ignore
    await ctx.respond(f"Added prefixes: {humanized_list_join(prefixes, conj='and')}")


@prefix_group.child
@lb.add_checks(lb.owner_only | lb.has_guild_permissions(hk.Permissions.ADMINISTRATOR))
@lb.option("prefix_", "The prefix to set")
@lb.command(
    "set",
    "Set a prefix, overriding the global prefix",
    aliases=["s"],
    pass_options=True,
)
@lb.implements(lb.PrefixSubCommand)
async def set_prefix(ctx: lb.Context, prefix_: str) -> None:
    await ctx.respond(f"Your set server prefix is: `{prefix_}`")


@prefix_group.child
@lb.add_checks(lb.owner_only | lb.has_guild_permissions(hk.Permissions.ADMINISTRATOR))
@lb.command(
    "reset", "Reset guild prefixes, revert back to global ones", aliases=["rst"]
)
@lb.implements(lb.PrefixSubCommand)
async def reset_prefix(ctx: lb.Context) -> None:
    await ctx.respond("Reset guild specifix prefixes")


@prefix_group.child
@lb.add_checks(lb.owner_only | lb.has_guild_permissions(hk.Permissions.ADMINISTRATOR))
@lb.option("prefix_", "The prefix to remove")
@lb.command("remove", "Remove a guild prefix", aliases=["rm"], pass_options=True)
@lb.implements(lb.PrefixSubCommand)
async def remove_prefix(ctx: lb.Context, prefix_: str) -> None:
    await ctx.respond(f"Removed the prefix {prefix_}")


@prefix_group.child
@lb.add_checks(lb.owner_only)
@lb.option("new_prefix", "Global prefix")
@lb.command("global", "Modify the global prefix", aliases=["g"], pass_options=True)
@lb.implements(lb.PrefixSubCommand)
async def change_global_prefix(ctx: lb.Context, new_prefix: str) -> None:
    await ctx.respond(f"Modified global prefix to: `{new_prefix}`")


def load(bot: lb.BotApp) -> None:
    """Load the plugin"""
    bot.add_plugin(prefix_manager)


def unload(bot: lb.BotApp) -> None:
    """Unload the plugin"""
    bot.remove_plugin(prefix_manager)
