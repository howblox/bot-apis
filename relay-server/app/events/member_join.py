import logging
from howblox_lib import fetch, StatusCodes, MemberSerializable
from howblox_lib.database import fetch_guild_data
from discord import Member
from app.howblox import howblox
from app.config import CONFIG


@howblox.event
async def on_member_join(member: Member):
    """Event for when a member joins a guild."""

    guild_data = await fetch_guild_data(member.guild.id, "autoRoles", "autoVerification", "highTrafficServer")

    if (guild_data.autoRoles or guild_data.autoVerification) and not guild_data.highTrafficServer:
        json_response, response = await fetch(
            "POST",
            f"{CONFIG.HTTP_BOT_API}/api/users/{member.id}/{member.guild.id}/join",
            headers={"Authorization": CONFIG.HTTP_BOT_AUTH},
            body={
                "member": MemberSerializable.from_discordpy(member).model_dump()
            },
            parse_as="JSON"
        )
        logging.debug(f"Relay server member join response: {response.status}, {json_response}")

        if response.status != StatusCodes.OK:
            logging.error(f"Relay server member join error: {response.status}, {json_response}")