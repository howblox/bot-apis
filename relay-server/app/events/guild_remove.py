import discord
from howblox_lib.database import update_guild_data
from app.howblox import howblox
from app.config import CONFIG


@howblox.event
async def on_guild_remove(guild: discord.Guild):
    """Event for when the bot leaves a guild."""

    if CONFIG.BOT_RELEASE == "PRO":
        await update_guild_data(guild.id, proBot=False)