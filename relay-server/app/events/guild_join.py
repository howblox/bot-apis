import logging
import discord
from howblox_lib import fetch_typed, StatusCodes
from howblox_lib.database import update_guild_data
from app.howblox import howblox
from app.types import PremiumResponse
from app.config import CONFIG



@howblox.event
async def on_guild_join(guild: discord.Guild):
    """Event for when the bot joins a guild."""

    await update_guild_data(guild.id, hasBot=True)

    if CONFIG.BOT_RELEASE == "PRO":
        json_response, response = await fetch_typed(
            PremiumResponse,
            f"{CONFIG.HTTP_BOT_API}/api/premium/guilds/{guild.id}",
            headers={"Authorization": CONFIG.HTTP_BOT_AUTH},
        )

        if json_response.premium and "pro" in json_response.features:
            await update_guild_data(guild.id, proBot=True)

        logging.debug(f"[Guild join] premium check response: {response.status}, {json_response}")

        if response.status != StatusCodes.OK:
            logging.error(f"[Guild join] premium check error: {response.status}, {json_response}")