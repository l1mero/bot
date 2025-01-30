import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict
from dotenv import load_dotenv
from os import getenv

load_dotenv()

uri = "172.17.0.1"
db = "bot"

class Motor:
    def __init__(self, collection: str, cache: bool = True):
        """
        Инициализация подключения к базе данных MongoDB.

        :param collection: Название коллекции MongoDB.
        """
        self.client = AsyncIOMotorClient(
            uri,
            username=getenv("MONGO_INITDB_ROOT_USERNAME"),
            password=getenv("MONGO_INITDB_ROOT_PASSWORD")
        )
        self.db = self.client[db]
        self.col = self.db[collection]
        self.cache = cache

        if cache:
            self.redis = redis.Redis(host='localhost', port=6379, password=getenv("REDIS_PASSWORD"))

    async def insert_one(self, document: Dict[str, Any]) -> str:
        """
        Вставка одного документа в коллекцию.

        :param document: Документ для вставки.
        :return: ID вставленного документа.
        """

        result = await self.col.insert_one(document)

        await self.redis.set(str(result.inserted_id), "gfgfgfgfgffgfg")

        return str(result.inserted_id)

    async def find_one(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Поиск одного документа по запросу.

        :param query: Запрос для поиска.
        :return: Найденный документ.
        """
        document = await self.col.find_one(query)
        return document

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """
        Обновление одного документа по запросу.

        :param query: Запрос для поиска документа.
        :param update: Обновления для документа.
        :return: True если обновление прошло успешно, иначе False.
        """
        result = await self.col.update_one(query, update)
        return result.modified_count > 0

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        """
        Удаление одного документа по запросу.

        :param query: Запрос для поиска документа.
        :return: True если удаление прошло успешно, иначе False.
        """

        result = await self.col.delete_one(query)
        return result.deleted_count > 0

    async def find_all(self, query: Dict[str, Any] = None) -> list:
        """
        Поиск всех документов по запросу.

        :param query: Запрос для поиска (по умолчанию пустой).
        :return: Список найденных документов.
        """

        documents = []
        async for document in self.col.find(query):
            documents.append(document)
        return documents
