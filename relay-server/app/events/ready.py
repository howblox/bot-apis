import logging
from app.howblox import howblox

@howblox.event
async def on_ready():
    """Log when the bot is ready."""
    logging.info(f"Logged in as {howblox.user.name}")