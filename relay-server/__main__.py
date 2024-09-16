import asyncio
from howblox_lib import load_modules
from app.howblox import howblox
from app.config import CONFIG


MODULES = (
    "app.web",
    "app.events",
    "app"
)


async def main():
    try:
        load_modules(*MODULES, starting_path="./")
    except FileNotFoundError: 
        load_modules(*MODULES, starting_path="./relay-server/")

    async with howblox as bot:
        await bot.start(CONFIG.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())