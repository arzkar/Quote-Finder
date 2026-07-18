from discord.ext import commands, tasks
from loguru import logger


class Keepalive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ping_qdrant.start()

    def cog_unload(self):
        self.ping_qdrant.cancel()

    @tasks.loop(hours=1)
    async def ping_qdrant(self):
        if not self.bot.vector_store:
            return
        try:
            await self.bot.vector_store.ping()
            logger.info("Qdrant keepalive ping succeeded.")
        except Exception as e:
            logger.warning(f"Qdrant keepalive ping failed: {e}")

    @ping_qdrant.before_loop
    async def before_ping_qdrant(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Keepalive(bot))
