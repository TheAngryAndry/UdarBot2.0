import asyncio

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie, UnionDoc
from aiogram.types import MenuButtonCommands
from apscheduler.jobstores.mongodb import MongoDBJobStore

import bot.loader as loader
from bot.utils.system import menu_button
from bot.utils.texts import load_words


async def main():
    # Connect to MongoDB
    client = AsyncIOMotorClient(f"mongodb://{loader.MONGO_USER}:{loader.MONGO_PASS}@{loader.MONGO_URI}"
                                if loader.MONGO_USER and loader.MONGO_PASS
                                else f"mongodb://{loader.MONGO_URI}")
    if client.database is None:
        logger.error("Failed to connect to MongoDB")
    logger.info("Starting bot...")
    loader.scheduler.add_jobstore(MongoDBJobStore(database=loader.MONGO_DB, collection='jobs'), collection='jobs')
    loader.scheduler.start()
    # Start bot and Beanie
    await asyncio.gather(
        loader.dp.start_polling(loader.bot),
        start_db(client)
    )


async def start_db(client: AsyncIOMotorClient):
    await init_beanie(
        database=client.get_database(loader.MONGO_DB),
        document_models=UnionDoc.__subclasses__() + Document.__subclasses__()
    ) if client.database is not None else None
    await load_words()


if __name__ == "__main__":
    # Set up logger
    logger.add(
        'logs/debug.log',
        level='DEBUG',
        format="{time} | {level} | {module}:{function}:{line} | {message}"
    )

    # Run main function in asyncio
    asyncio.run(main(), debug=True)
