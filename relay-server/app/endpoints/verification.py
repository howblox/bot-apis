import logging
from howblox_lib import BaseModel, fetch, StatusCodes
from ..base import RelayEndpoint
from ..config import CONFIG
from ..redis import RedisRelayRequest
from ..howblox import howblox
from ..types import Response



class Payload(BaseModel):
    """Payload for the verification endpoint."""

    user_id: int
    guild_ids: list[int]


class VerificationEndpoint(RelayEndpoint[Payload]):
    """An endpoint for remotely updating a user.

    TODO: make this an endpoint on the http bot itself after MVP. This is on the relay server for compatibility with API.

    """

    def __init__(self):
        super().__init__("VERIFICATION", Payload)

    async def handle(self, request: RedisRelayRequest[Payload]) -> Response:
        payload = request.payload
        guild_ids = payload.guild_ids
        user_id = payload.user_id

        for guild_id in guild_ids: # TODO: probably unnecessary to handle from relay server. might be better for API -> http bot directly.
            guild = howblox.get_guild(guild_id)

            if not guild:
                continue

            text, response = await fetch(
                "POST",
                f"{CONFIG.HTTP_BOT_API}/api/users/{user_id}/update",
                headers={"Authorization": CONFIG.HTTP_BOT_AUTH},
                body={
                    "guild_id": guild.id,
                    "member_id": user_id,
                    "dm_user": False
                },
                raise_on_failure=False
            )

            if response.status != StatusCodes.OK:
                logging.error(f"Verification endpoint response: {response.status}, {text}")


        return Response(success=True)