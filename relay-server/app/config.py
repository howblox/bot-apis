from typing import Literal
from os import getcwd, environ
from dotenv import load_dotenv
from howblox_lib import Config as HOWBLOX_CONFIG, get_environment

load_dotenv(f"{getcwd()}/.env")

__all__ = ("CONFIG",)

class Config(HOWBLOX_CONFIG):
    """Type definition for config values."""

    #############################
    PLAYING_STATUS: str = "/invite | howblox.net"
    SHARD_COUNT: int = 1
    SHARDS_PER_NODE: int = 1
    BOT_RELEASE: Literal["LOCAL", "CANARY", "MAIN", "PRO"]
    HTTP_BOT_API: str
    HTTP_BOT_AUTH: str

    PORT: int = 8020
    HOST: str = "0.0.0.0"

    def model_post_init(self, __context):
        if get_environment() != "STAGING":
            if self.SHARD_COUNT < 1:
                raise ValueError("SHARD_COUNT must be at least 1")

            if self.SHARDS_PER_NODE < 1:
                raise ValueError("SHARDS_PER_NODE must be at least 1")



CONFIG: Config = Config(
    **{field:value for field, value in environ.items() if field in Config.model_fields}
)